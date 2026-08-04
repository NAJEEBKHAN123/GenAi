from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# 1. Gemini LLM
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)


# --------------------------------------------------
# 2. Create Tool
# --------------------------------------------------

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# ------------------------------------------------
# 3. Test the tool directly
# ------------------------------------------------

tool_result = multiply.invoke({
    "a": 5,
    "b": 8
})



# --------------------------------------------------
# 4. Bind tool to Gemini
# --------------------------------------------------

llm_tool = llm.bind_tools([multiply])


# --------------------------------------------------
# 5. User message
# --------------------------------------------------

query = HumanMessage(
    content="Can you multiply 5 with 10?"
)

messages = [query]


# --------------------------------------------------
# 6. Ask Gemini
# --------------------------------------------------

ai_message = llm_tool.invoke(messages)

print("AI message:")
print(ai_message)

print("\nTool calls:")
print(ai_message.tool_calls)


# --------------------------------------------------
# 7. Execute the tool
# --------------------------------------------------

tool_call = ai_message.tool_calls[0]

tool_message = multiply.invoke(tool_call)

print("\nTool result:")
print(tool_message)


# --------------------------------------------------
# 8. Add tool result to conversation
# --------------------------------------------------

messages.append(ai_message)
messages.append(tool_message)


# --------------------------------------------------
# 9. Ask Gemini for final answer
# --------------------------------------------------

final_response = llm_tool.invoke(messages)

print("\nFinal response:")
print(final_response.content)