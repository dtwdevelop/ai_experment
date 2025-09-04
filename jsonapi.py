from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings , ChatOllama
from langchain_core.messages import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
url = "all.json"
loader = JSONLoader(file_path=url,  jq_schema='[.[].name.common]', text_content=False)
docs = loader.load()
store = FAISS.from_documents(docs, embedding=OllamaEmbeddings(model="llama3.1"))

retriever = store.as_retriever(search_type="similarity", search_kwargs={"k": 1})

llm = ChatOllama(model="llama3.1")
message = """
{question}
Context:
{context}
"""
prompt = ChatPromptTemplate([
    ("system", "You bot who search documents"),
    ("human", message),
])
parser = StrOutputParser
chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm
messages = [
    HumanMessage(content="css")
]
print("Print information from file")
ask = input("Ask about countries :")
for ch in chain.stream(ask):
    print(ch.content, end="")