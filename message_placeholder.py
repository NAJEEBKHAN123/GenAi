from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


chat_template = ChatPromptTemplate([
    ('system', 'You are a helpful customer agent.'),
    MessagesPlaceholder(variable_name='chat_history'),
    ("user", "{query}")
])


chat_history = []

#load chat history 

with open('chat_history.txt') as f:
    chat_history.extend(f.readlines())

print(chat_history)


#create prompt

chat_prompt = chat_template.invoke({
    'chat_history': chat_history,
    'query': 'Where is my refund ?'
})

print(chat_prompt)