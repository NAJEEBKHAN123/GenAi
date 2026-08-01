from langchain_community.document_loaders import UnstructuredPDFLoader

# Best for scanned/image PDFs and structure extraction
loader = UnstructuredPDFLoader('scanned_document.pdf', mode="single")

docs = loader.load()

print(f"Loaded {len(docs)} pages")
print(docs[0].page_content[:500])  # First 500 chars of first page
