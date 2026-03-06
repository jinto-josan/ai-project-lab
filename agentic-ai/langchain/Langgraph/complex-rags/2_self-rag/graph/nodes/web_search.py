from typing import Any, Dict
from dotenv import load_dotenv
from graph.state import GraphState
from graph.chains.retriever_grader import GradeDocuments, retriever_grader
from langchain_tavily import TavilySearch

web_search_tool=TavilySearch(max_results=3)
load_dotenv()

def web_search_node(state:GraphState)->Dict[str, Any]:
    question=state["question"]
    documents=state["documents"]

    tavily_results=web_search_tool.invoke({"query": question})
    joined_results="\n\n".join([result["content"] for result in tavily_results])
    web_results=Document(page_content=joined_results, metadata={"source": "tavily"})
    if documents is not None:
        documents.append(web_results)
    else:
        documents=[web_results]
    return {"documents": documents, "question": question}



if __name__ == "__main__":
    web_search_node({"question": "hallucination", "documents": None})