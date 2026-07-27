import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash"
)

result = model.invoke("What is the capital of France?")

if isinstance(result.content, list):
    for block in result.content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block.get("text"))
        elif isinstance(block, str):
            print(block)
else:
    print(result.content)