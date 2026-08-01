from langchain_community.document_loaders import PDFPlumberLoader

# Best for PDFs with tables and columns
loader = PDFPlumberLoader('document_with_tables.pdf')

docs = loader.load()

print(f"Loaded {len(docs)} pages")
print(docs[0].page_content[:500])  # First 500 chars of first page
