from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from typing import List

load_dotenv()

def ingest_data(urls:List[str])->None:
    loaded_documents=[WebBaseLoader(url).load() for url in urls]
    documents=[item for sublist in loaded_documents for item in sublist]
    text_splitter=RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)
    texts=text_splitter.split_documents(documents)
    embeddings=OllamaEmbeddings(model="qwen3-embedding")
    Chroma.from_documents(documents=texts, embedding=embeddings, collection_name="langchain", persist_directory="./Langgraph/complex-rags/1_corrective-rag/.chroma_db")

retriever= Chroma(persist_directory="./Langgraph/complex-rags/1_corrective-rag/.chroma_db", 
embedding_function=OllamaEmbeddings(model="qwen3-embedding")).as_retriever()


if __name__ == "__main__":
    ingest_data(["https://lilianweng.github.io/posts/2025-05-01-thinking/", 
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/", "https://lilianweng.github.io/posts/2024-07-07-hallucination/"])
    