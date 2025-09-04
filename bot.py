from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

model = ChatOllama(model="llama3.1")

message_history = RunnableWithMessageHistory(model , get_session_history)

aimessage = AIMessage(content='Hi i\'m Spamer , I bot how can help you')
sysmessage  = SystemMessage(content="Speak russian")
config = {"configurable": {"session_id": "abc2"}}
data = ""
while data != "/exit":
    data = input("Запрос: ")
    for res in message_history.stream([ sysmessage , aimessage, HumanMessage(content=data)], config=config,):
        print(res.content , end="" , flush=True)
