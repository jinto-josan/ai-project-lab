from typing import Any, Dict
from state import GraphState
from ingestion import retriever


def retrieve_node(state:GraphState)->Dict[str, Any]:
    question=state["question"]
    documents=retriever.invoke(question)
    return {"documents": documents, "question": question}