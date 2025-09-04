from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import random

SQL_PREFIX = """
You mysql client  agent
Find item from product table and  relationship with foreign key category_id to table  category 
Only use the information returned by the below tools to construct your final answer.

Return only 1 result json  object with fields  name title color and price   

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
To start you should ALWAYS look at the tables in the database to see what you can query.
Do NOT skip this step.
Then you should query the schema of the most relevant tables.
"""
system_message = SystemMessage(content=SQL_PREFIX)
llm = ChatOllama(model="llama3.1")

# llm = ChatOllama(model="mistral")
# db = SQLDatabase.from_uri("sqlite:///Chinook.db")
ps = ""
db = SQLDatabase.from_uri(f"mysql+pymysql://root:{ps}@localhost:33060/sample")
print(db.get_usable_table_names())
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
memory = MemorySaver()
config = {"configurable": {"thread_id": "abc" + str(random.random())}}
agent = create_react_agent(llm, tools, messages_modifier=system_message, checkpointer=memory)
resText = ""
ask = input("Ask me: ")
sp = "."
for ch in agent.stream({"messages": [HumanMessage(content=ask)]}, config=config):
    print(f"Loading {sp}")
    sp += "."
    resText = ch
print(resText['agent']['messages'][0].content)
