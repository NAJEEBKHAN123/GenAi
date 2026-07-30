from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

schema = {
    "title": "Person",
    "description": "Information about a person",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The person's full name"
        },
        "age": {
            "type": "integer",
            "description": "The person's age"
        },
        "city": {
            "type": "string",
            "description": "The city where the person lives"
        }
    },
    "required": ["name", "age", "city"]
}

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",   # or another model available to your API key
    temperature=0
)

structured_llm = llm.with_structured_output(schema)

result = structured_llm.invoke(
    "John is 25 years old and lives in London."
)

print(result)