#Langchain_API_KEY = "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"

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama


import streamlit as st
import os 
from dotenv import load_dotenv

load_dotenv()

os.environ["Langchain_API_KEY"] = os.getenv("Langchain_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"

##creating chatbot

prompt =  ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please provide response to the user queries"),
        ("user","Question:{question}")

    ]
)
#stramlit framework
st.title("Langchain demo with Llama2 api")
input_text = st.text_input("Search the topic you want")

#LLM CALL
llm = Ollama(model="llama2")
output_parser = StrOutputParser()

##chain
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))