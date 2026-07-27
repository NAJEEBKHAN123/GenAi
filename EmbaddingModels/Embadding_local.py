import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

if os.getenv("HUGGINGFACEHUB_API_KEY"):
    os.environ["HF_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_KEY")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)


text = "What is the capital of France?"

query_vector = embeddings.embed_query(text)

print(f"Query: '{text}'")
print(f"Embedding Vector Dimension: {len(query_vector)}")
