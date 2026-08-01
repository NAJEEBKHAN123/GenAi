from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings


embadding = HuggingFaceEmbeddings(
     model_name="sentence-transformers/all-MiniLM-L6-v2"
)


splitter = SemanticChunker(
    embadding,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=90
)

text = """
Python is a popular programming language.
It is widely used for web development.
Python is also used in artificial intelligence and machine learning.

Machine learning allows computers to learn from data.
Deep learning is a subset of machine learning.
Neural networks are commonly used in deep learning.

The Eiffel Tower is located in Paris.
It was completed in 1889.
It is one of the most famous landmarks in the world.

I'm from bajaur and i want to become a AI Engr. 
Do you like me or not ?
"""

chunks = splitter.split_text(text)

print(len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)