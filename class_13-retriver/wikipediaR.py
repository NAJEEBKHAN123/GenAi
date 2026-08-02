# Wikipedia Retriever using LangChain

from langchain_community.retrievers import WikipediaRetriever

retriever = WikipediaRetriever(top_k_results=2)

query = "What is the capital of France?"

docs = retriever.invoke(query)

print(f"Number of documents retrieved: {len(docs)}")

for i, doc in enumerate(docs, 1):
    print(f"\n--- Document {i} ---")
    print(doc.page_content)
    print("Metadata:", doc.metadata)