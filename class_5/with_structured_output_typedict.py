from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class review(TypedDict):
    summary: str
    sentiment: str

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

structured_llm = llm.with_structured_output(review)

result = structured_llm.invoke(
    "The phone has an excellent camera but the battery drains quickly."
)

print(result)