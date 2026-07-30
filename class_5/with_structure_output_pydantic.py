from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class Person(BaseModel):
    name: str
    age: int
    city: str

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)

structured_llm = llm.with_structured_output(Person)

result = structured_llm.invoke("John is 25 years old and lives in London.")

print(result)

print(result.name)
print(result.age)
print(result.city)