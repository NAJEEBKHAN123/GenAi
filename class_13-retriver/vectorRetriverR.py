from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


# Initialize the embedding model
model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

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

# Create a Chroma vector store
vector_store = Chroma.from_documents(
    documents=documents,
    embedding=model,
    collection_name="cricket_players"
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

query = "Who is a bowler among these players?"

result = retriever.invoke(query)

for i, doc in enumerate(result, 1):
    print(f"\n--- Result {i} ---")
    print(doc.page_content)