from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import sklearn.metrics.pairwise as pairwise
import numpy as np
load_dotenv()


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

documents = [
    "Paris is the capital of France.",
    "Berlin is the capital of Germany.",
    "Tokyo is the capital of Japan.",
    "London is the capital of the United Kingdom.",
    "Washington, D.C. is the capital of the United States."

]

query = "Tell me about the France ?"


# Embed the documents and the query
doc_vectors = embeddings.embed_documents(documents)
query_vector = embeddings.embed_query(query)

cosine_similarities = pairwise.cosine_similarity([query_vector], doc_vectors)

# Get the index of the most similar document
most_similar_index = np.argmax(cosine_similarities)

print(f"Most similar document: {documents[most_similar_index]}")