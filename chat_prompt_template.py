from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate([
    ('system', 'You are a helpful {domain} assistant.'),
    ('user', 'Explain the following question: {question}'),
])


prompt = chat_template.invoke({
    'domain': 'science',
    'question': 'What is the speed of light?'}) 


print(prompt)