from typing import Any, Dict

from graph.state import GraphState
from graph.chains.generation_chain import generation_chain

def generate_node(state: GraphState) -> Dict[str, Any]:
    question = state["question"]
    documents = state["documents"]
    # Format documents list into a single string
    context = "\n\n".join(documents) if documents else ""
    generation = generation_chain.invoke({"question": question, "context": context})
    return {"generation": generation, "question": question, "documents": documents}