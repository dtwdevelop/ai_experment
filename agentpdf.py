from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings , ChatOllama
from langchain_core.messages import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import CharacterTextSplitter

from langchain_chroma import Chroma
file_path = ("python.pdf")
loader = PyPDFLoader(file_path)
print("Load file")
splitter = CharacterTextSplitter( separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len)
pages = loader.load_and_split(text_splitter=splitter)
print("Split file finished")
store = FAISS.from_documents(pages, embedding=OllamaEmbeddings(model="llama3.1"))
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
for ch in chain.stream("def function"):
    print(ch.content, end="")