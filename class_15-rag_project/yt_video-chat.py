from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate



model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


video_id = "Gfr50f6ZBvo"

try:
    api = YouTubeTranscriptApi()

    transcript_data = api.fetch(
        video_id,
        languages=["en"]
    )

    transcript_list = transcript_data.to_raw_data()

    transcript = " ".join(
        chunk["text"] for chunk in transcript_list
    )

    # print(
    #     "Transcript fetched successfully.",
    #     f"Length: {len(transcript)} characters."
    #     "..."
    # )

except TranscriptsDisabled:
    print("Transcripts are disabled for this video.")


    # step 1: Split the transcript into smaller chunks

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,

)

chunks = text_splitter.create_documents([transcript])

# print(chunks[0], "chunks created from the transcript.")


#indexing ( embedding generation and storing in vector database)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

result = vector_store.index_to_docstore_id
# print(result, "result of indexing the transcript chunks into the vector store.")


# retrieval (searching for relevant chunks based on a query)

retriever = vector_store.as_retriever(
    search_type="similarity"
)

# print(retriever)

result1 = retriever.invoke('What is deepmind')

# print(result1[0].page_content)

# AUGMENTATION

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
    If the context if insufficient, say "I don't know".
    Context: {context}
    Question: {question}
    Answer:
    """,
    input_variables=["context", "question"]
)

question = "Is the topic of aliens discussed in this video? If yes then what was discussed"
retrieved_docs = retriever.invoke(question)

context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
final_prompt = prompt.invoke({"context": context_text, "question": question})

# print(final_prompt)

# step 4- Generations

answer = llm.invoke(final_prompt)
# print(answer)






# Building a chain 

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

def format_docs(retrieved_docs):
    context_text = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )
    return context_text

parallel_chain = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

parallel_chain.invoke('who is Demis')
# print(parallel_chain)


parser = StrOutputParser()

main_chain = parallel_chain | prompt | llm | parser


chain =  main_chain.invoke('can you summarize the video?')
print(chain)