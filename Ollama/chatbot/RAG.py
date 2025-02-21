import os
import streamlit as st
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader


load_dotenv()


os.environ["Langchain_API_KEY"] = os.getenv("Langchain_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"


llm = Ollama(model="llama2")


text_loader = TextLoader("knowledge_base.txt")  # Create and store your knowledge in this file
documents = text_loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)


embeddings = OpenAIEmbeddings()  # Requires OpenAI API key
vector_store = FAISS.from_documents(chunks, embeddings)
retriever = vector_store.as_retriever()


qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please provide responses to user queries."),
        ("user", "Question: {question}")
    ]
)


st.title("LangChain + RAG with Llama 2")
input_text = st.text_input("Ask a question:")

if input_text:
    response = qa_chain.run(input_text)  
    st.write(response)
