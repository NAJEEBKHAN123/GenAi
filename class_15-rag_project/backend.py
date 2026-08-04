from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import re

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store the RAG pipeline
vector_store = None
retriever = None
llm = None
prompt = None
main_chain = None

class ProcessVideoRequest(BaseModel):
    video_url: str

class ProcessVideoResponse(BaseModel):
    success: bool
    video_id: str
    message: str

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def format_docs(retrieved_docs):
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return context_text

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    global llm, prompt
    print("Loading LLM...")
    llm = HuggingFacePipeline.from_model_id(
        model_id="Qwen/Qwen2.5-0.5B-Instruct",
        task="text-generation",
        pipeline_kwargs={
            "temperature": 0.2,
            "max_new_tokens": 512,
        }
    )
    prompt = PromptTemplate(
        template="""
        You are a helpful assistant. 
        Answer ONLY from the provided transcript context.
        If the context is insufficient, say "I don't know".
        Context: {context}
        Question: {question}
        Answer:
        """,
        input_variables=["context", "question"]
    )
    print("Models loaded successfully!")

@app.post("/process-video", response_model=ProcessVideoResponse)
async def process_video(request: ProcessVideoRequest):
    """Process a YouTube video and create RAG pipeline"""
    global vector_store, retriever, main_chain
    
    try:
        # Extract video ID
        video_id = extract_video_id(request.video_url)
        if not video_id:
            print(f"Failed to extract video ID from URL: {request.video_url}")
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        print(f"Processing video: {video_id}")
        
        # Fetch transcript
        try:
            api = YouTubeTranscriptApi()
            transcript_data = api.fetch(video_id, languages=["ur", "hi", "en"])
            transcript_list = transcript_data.to_raw_data()
            transcript = " ".join(chunk["text"] for chunk in transcript_list)
            print(f"Transcript fetched successfully. Length: {len(transcript)} characters")
        except TranscriptsDisabled:
            print("Transcripts disabled for this video")
            raise HTTPException(status_code=400, detail="This video does not have transcripts available. Please try a different video.")
        except Exception as e:
            print(f"Failed to fetch transcript: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to fetch transcript. The video might not have transcripts or YouTube is blocking the request. Please try a different video.")
        
        # Split transcript
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.create_documents([transcript])
        print(f"Created {len(chunks)} chunks")
        
        # Create embeddings and vector store
        print("Creating embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        vector_store = FAISS.from_documents(chunks, embeddings)
        print("Vector store created")
        
        # Create retriever
        retriever = vector_store.as_retriever(search_type="similarity")
        
        # Create RAG chain
        parallel_chain = RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        })
        
        parser = StrOutputParser()
        main_chain = parallel_chain | prompt | llm | parser
        
        print(f"Video processed successfully: {video_id}")
        return ProcessVideoResponse(
            success=True,
            video_id=video_id,
            message="Video processed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """Ask a question about the processed video"""
    if not main_chain:
        raise HTTPException(status_code=400, detail="No video has been processed yet")
    
    try:
        print(f"Processing question: {request.question}")
        result = main_chain.invoke(request.question)
        
        # Extract just the answer part (remove the prompt if it's included)
        answer = str(result).strip()
        
        # Remove common prompt artifacts
        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()
        if "Context:" in answer:
            answer = answer.split("Context:")[-1].strip()
        
        # Remove any remaining prompt template text
        prompt_markers = [
            "You are a helpful assistant",
            "Answer ONLY from the provided transcript context",
            "If the context is insufficient",
            "Question:"
        ]
        for marker in prompt_markers:
            if marker in answer:
                parts = answer.split(marker)
                if len(parts) > 1:
                    answer = parts[-1].strip()
        
        print(f"Answer generated: {answer[:100]}...")
        return AskResponse(answer=answer)
    except Exception as e:
        print(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "YouTube RAG Backend API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
