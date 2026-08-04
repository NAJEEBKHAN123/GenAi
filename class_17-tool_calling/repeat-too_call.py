from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv


load_dotenv()

## step 1

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)

## step 2

@tool 

def multiply(a: int, b: int) -> int:
    """multiply two numbers"""
    return a * b

test = multiply.invoke(({'a': 5, 'b': 6}))


## step 3

llm_tool = llm.bind_tools([multiply])


### step 4

query = HumanMessage(
    content="Multiply the 6 with 8 ?"
)

messages = [query]

## step 5

ai_message = llm_tool.invoke(messages)

# print('AI message: ', ai_message)


# step 6

tool_call = ai_message.tool_calls[0]
tool_message = multiply.invoke(tool_call)

#final messge

final_response = llm_tool.invoke(messages)
