from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Initialize the embedding model
model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create documents
doc1 = Document(
    page_content="""
    Rohit Sharma is an Indian cricketer and opening batter.
    He is known for his excellent timing, pull shots, and leadership skills.
    He has played for Mumbai Indians in the IPL.
    """,
    metadata={
        "player": "Rohit Sharma",
        "team": "Mumbai Indians",
        "country": "India"
    }
)

doc2 = Document(
    page_content="""
    Virat Kohli is an Indian cricketer and one of the most consistent
    batters in modern cricket. He is known for his aggressive batting,
    fitness, and ability to chase targets.
    He plays for Royal Challengers Bengaluru in the IPL.
    """,
    metadata={
        "player": "Virat Kohli",
        "team": "Royal Challengers Bengaluru",
        "country": "India"
    }
)

doc3 = Document(
    page_content="""
    Jasprit Bumrah is an Indian fast bowler known for his unique bowling
    action, accurate yorkers, pace variations, and excellent death bowling.
    He plays for Mumbai Indians in the IPL.
    """,
    metadata={
        "player": "Jasprit Bumrah",
        "team": "Mumbai Indians",
        "country": "India"
    }
)

doc4 = Document(
    page_content="""
    Ravindra Jadeja is an Indian all-rounder known for his left-handed
    batting, left-arm spin bowling, and excellent fielding.
    He plays for Chennai Super Kings in the IPL.
    """,
    metadata={
        "player": "Ravindra Jadeja",
        "team": "Chennai Super Kings",
        "country": "India"
    }
)

docs = [doc1, doc2, doc3, doc4]

# print(docs[0].page_content)

# CORRECTION 1: Use the model itself, not model.embed_documents
vector_store = Chroma(
    embedding_function=model,  
    persist_directory="chroma_db",
    collection_name='cricket_players'
)

# Add documents and get their IDs
v1 = vector_store.add_documents(docs)
# print(v1)  

# CORRECTION 2: get() method - embeddings might not be stored by default
# Use this instead if you want to retrieve documents
all_docs = vector_store.get()
# print(all_docs)

# Search for bowlers
bowler = vector_store.similarity_search(
    query="who among these are a bowler",
    k=2
)
# print("Bowler search results:", bowler)

# CORRECTION 3: Fix the filter - it should be 'Mumbai Indians' (plural)
bowler1 = vector_store.similarity_search_with_score(
    query="",  # Empty query is fine, but you might want to add something
    filter={'team': 'Mumbai Indians'}  # Changed from 'Mumbai Indian'
)
# print("Filtered results:", bowler1)


doc2_id = v1[1]  # Get the ID from the add_documents return

doc2_updated = Document(
    page_content="virat kohli is mostly the player of the match when they score 50+",
    metadata={
        "player": "Virat Kohli",  # CORRECTION 5: This should be Virat Kohli, not Rohit Sharma
        "team": "Royal Challengers Bengaluru",
        "country": "India"
    }
)

# Update the document
vector_store.update_document(document_id=doc2_id, document=doc2_updated)

# CORRECTION 6: Delete document - you need a valid ID
# Example: delete the first document
if v1:  # Check if there are any documents
    vector_store.delete(ids=[v1[0]])  # Delete the first document

# Optional: Verify the deletion by getting all documents
remaining_docs = vector_store.get()
print("Remaining documents after deletion:", remaining_docs)