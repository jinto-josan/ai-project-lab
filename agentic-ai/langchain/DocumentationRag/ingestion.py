import os
from dotenv import load_dotenv
import asyncio
import ssl
from typing import Any,Dict, List, Optional, Tuple, Union
import certifi

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_tavily import TavilyCrawl,TavilyExtract, TavilyMap
from langchain_core.documents import Document

from custom_logging import (Colors, log_info, log_error, log_warning, log_success, log_header)

load_dotenv()

#Configure ssl context to use certifi's CA bundle for secure connections
ssl_context = ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

embeddings = OllamaEmbeddings(model="qwen3-embedding")
vector_store = PineconeVectorStore(embedding    =embeddings, index_name=os.environ["INDEX_NAME"])
tavily_extract= TavilyExtract()
tavily_map= TavilyMap( max_depth=5, max_breadth=20, max_pages=10000)
tavily_crawl=TavilyCrawl()

async def main():
    """Main function to run the ingestion process asynchronously."""
    log_header("DOCUMENT INGESTION PIPELINE")

    log_info("Tavily Crawl crawling https://docs.langchain.com/")

    #Crawl the document site
    res = tavily_crawl.invoke({
        "url": "https://docs.langchain.com/",
        "max_depth": 5,
        "extract_depth": "advanced", #extracts table, embeds, more data and takes more time.
        #"instructions": if certain pages need to be prioritized, we can provide instructions to tavily map to prioritize those pages. For example, if we want to prioritize the "Getting Started" page, we can provide the following instructions: "Prioritize crawling and extracting content from the 'Getting Started' page and its subpages."
    })
    all_docs = res["documents"]
    log_success(f"Crawled {len(all_docs)} documents.")


    log_header("Document Chunking...")
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=200
    )

    # Split documents into chunks
    splitted_docs= text_splitter.split_documents(all_docs)

    log_success(f"Created {len(splitted_docs)} document chunks.")
    await store_in_vector_store(splitted_docs, batch_size=500)

    

async def store_in_vector_store(docs: List[Document], batch_size: int = 50):
    """Asynchronously store documents in the vector store."""
    log_header("Storing in Vector Store...")

    #Create batches of documents to store in the vector store
    batches= [docs[i:i + batch_size] for i in range(0, len(docs), batch_size)]
    
    #Process batches concurrently using asyncio.gather
    async def store_batch(batch: List[Document], batch_num: int):
        """Store a batch of documents in the vector store."""
        try:
            await vector_store.aadd_documents(batch)
            log_success(f"Batch {batch_num} stored successfully with {len(batch)} documents.")
        except Exception as e:
            log_error(f"Error storing batch {batch_num}: {str(e)}")
            return False
        return True
    tasks = [store_batch(batch, idx) for idx, batch in enumerate(batches)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    #Count successful and failed batches
    success_count = sum(1 for result in results if result is True)
    failure_count = sum(1 for result in results if result is False)


if __name__ == "__main__":
    asyncio.run(main())