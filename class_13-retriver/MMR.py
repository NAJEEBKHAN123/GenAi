from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface.embeddings.huggingface import HuggingFaceEmbeddings


# Create documents
documents = [
    Document(
    page_content="""
    Rohit Sharma is an Indian cricketer and opening batter.
    He is known for his excellent timing, pull shots, and leadership skills.
    He has played for Mumbai Indians in the IPL.
    """),
    Document(
    page_content="""
    Virat Kohli is an Indian cricketer and one of the most consistent
    batters in modern cricket. He is known for his aggressive batting,
    fitness, and ability to chase targets.
    He plays for Royal Challengers Bengaluru in the IPL.
    """),
    Document(
    page_content="""
    Jasprit Bumrah is an Indian fast bowler known for his unique bowling
    action, accurate yorkers, pace variations, and excellent death bowling.
    He plays for Mumbai Indians in the IPL.
    """),
    Document(
    page_content="""
    Ravindra Jadeja is an Indian all-rounder known for his left-handed
    batting, left-arm spin bowling, and excellent fielding.
    He plays for Chennai Super Kings in the IPL.
    """)
]

model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create a FAISS vector store
vector_store = FAISS.from_documents(
    documents=documents,
    embedding=model
)

retriver = vector_store.as_retriever(
    search_type='mmr',
    search_kwargs={'k': 2, 'lambda_mult': 1}
)

query = "Who is a batter among these players?"
result = retriver.invoke(query)

for i, doc in enumerate(result, 1):
    print(f"\n--- Result {i} ---")
    print(doc.page_content)