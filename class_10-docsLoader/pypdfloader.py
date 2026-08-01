from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('Letter_to_the_Editor.pdf')

pdf = loader.load()

print(pdf[0].page_content)
print(len(pdf))
