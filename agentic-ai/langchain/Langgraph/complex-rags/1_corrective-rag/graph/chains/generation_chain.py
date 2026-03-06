from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain import hub


load_dotenv()

llm=ChatOllama(model="qwen3:1.7b", temperature=0)
prompt=hub.pull("langchain-ai/rag-prompt")
generation_chain= prompt | llm | StrOutputParser()