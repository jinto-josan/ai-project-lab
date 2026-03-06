from typing import List,TypedDict


class GraphState(TypedDict):
    """State for the graph"""

    question: str
    generation: str
    websearch: str
    documents: List[str]