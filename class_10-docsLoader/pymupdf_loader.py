from langchain_community.document_loaders import PyMuPDFLoader

# Best when you need layout and image data
loader = PyMuPDFLoader('document_with_images.pdf')

docs = loader.load()

print(f"Loaded {len(docs)} pages")
print(docs[0].page_content[:500])  # First 500 chars of first page
