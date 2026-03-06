from typing import Any, Dict

from graph.state import GraphState
from graph.chains.generation_chain import generation_chain
def generate_node(state:GraphState)->Dict[str, Any]:
    question=state["question"]
    documents=state["documents"]
    generation=generation_chain.invoke({"question": question, "context": documents})
    return {"generation": generation, "question": question, "documents": documents}