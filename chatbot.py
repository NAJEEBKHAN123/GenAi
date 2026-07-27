from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFacePipeline.from_model_id(
    model_id="Qwen/Qwen2.5-0.5B-Instruct",
    task="text-generation",
)

model = ChatHuggingFace(llm=llm)
chat_history = []

print("Chatbot started (type 'exit' to quit)")

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break
    
    # Add user message to history
    chat_history.append(HumanMessage(content=user_input))
    
    # Get response
    result = model.invoke(chat_history)
    
    # Add AI response to history
    chat_history.append(AIMessage(content=result.content))
    
    print("Bot:", result.content)


