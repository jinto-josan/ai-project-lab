import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

if __name__ == "__main__":
    print("Ingesting...")

    loader = TextLoader("/Users/jinto/Desktop/Repositories/Personal/ai-project-lab/agentic-ai/langchain/Rag/mediumblog.txt")
    documents = loader.load()
    
    print("Splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0) #choose value such that chunk has semantic meaning
    texts = text_splitter.split_documents(documents)

    print("Embedding...")
    embeddings = OllamaEmbeddings(model="qwen3-embedding")

    print("Storing...")
    PineconeVectorStore.from_documents(texts, embeddings, index_name=os.environ["INDEX_NAME"])