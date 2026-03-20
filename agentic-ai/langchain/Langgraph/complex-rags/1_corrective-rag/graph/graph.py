from dotenv import load_dotenv
from graph.state import GraphState
from graph.nodes import retrieve_node, grade_documents_node, web_search_node, generate_node
from graph.constants import RETRIEVE, GRADE_DOCUMENTS, WEB_SEARCH, GENERATION
from langgraph.graph import StateGraph, END




load_dotenv()

def decide_to_generate(state:GraphState)->str:
    if state["websearch"]:
        return WEB_SEARCH
    else:
        return GENERATION

workflow=StateGraph(GraphState)
workflow.add_node(RETRIEVE, retrieve_node)
workflow.add_node(GRADE_DOCUMENTS, grade_documents_node)
workflow.add_node(WEB_SEARCH, web_search_node)
workflow.add_node(GENERATION, generate_node)


workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(GRADE_DOCUMENTS, decide_to_generate, 
    {
    GENERATION: GENERATION,
    WEB_SEARCH: WEB_SEARCH}
)
workflow.add_edge(WEB_SEARCH, GENERATION)
workflow.add_edge(GENERATION, END)
app=workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path="./Langgraph/complex-rags/1_corrective-rag/flow.png")