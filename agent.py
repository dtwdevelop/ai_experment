from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage
import os
import pyttsx3
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.output_parsers import StrOutputParser
import json

def Speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()

# os.environ["TAVILY_API_KEY"] = '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'
# search = TavilySearchResults(max_results=2)

search = DuckDuckGoSearchRun()

# search_results = search.invoke("what is the weather in London")
# print(search_results)
memory = MemorySaver()
tools = [search]
model = ChatOllama(model="llama3.1")
# wit_tool = model.bind_tools(tools)
res_text = ""
system = SystemMessage(content='Translate to russian')
ask = input("Ask about:")
agent = create_react_agent(model, tools, checkpointer=memory)
data = {"messages": [HumanMessage(content=ask)]}
config = {"configurable": {"thread_id": "abc123"}}
res = ""
parser = StrOutputParser()
for ch in agent.stream(data, config):
   print('Loading ...')
   # print(ch)
   res = ch

speak_me = res['agent']['messages'][0].content
print(speak_me)

# Speak(speak_me)