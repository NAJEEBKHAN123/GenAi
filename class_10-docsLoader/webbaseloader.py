import os
# 1. Set the user agent to prevent target servers from blocking your request
os.environ["USER_AGENT"] = "MyLangChainApp/1.0"

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader('https://applemac.pk/product/iphone-17e-256gb-white')

docs = loader.load()

print(len(docs))
print(docs[0].page_content)