from langchain_community.document_loaders import AmazonTextractPDFLoader

# Best for scanned/image PDFs (requires AWS credentials)
loader = AmazonTextractPDFLoader('scanned_document.pdf')

docs = loader.load()

print(f"Loaded {len(docs)} pages")
print(docs[0].page_content[:500])  # First 500 chars of first page
