from dotenv import load_dotenv
from graph.state import GraphState
from graph.nodes import retrieve_node, grade_documents_node, web_search_node, generate_node
from graph.constants import RETRIEVE, GRADE_DOCUMENTS, WEB_SEARCH, GENERATION
from langgraph.graph import StateGraph, END

from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.answer_grader import answer_grader


load_dotenv()

def decide_to_generate(state:GraphState)->str:
    if state["websearch"]:
        return WEB_SEARCH
    else:
        return GENERATION

def grade_generation_grounded_in_documents_and_question(state:GraphState)->str:
    question=state["question"]
    documents=state["documents"]
    generation=state["generation"]
    score= hallucination_grader.invoke({"documents": documents, "generation": generation})
    if hallucination_score:=score.binary_score:
        score = answer_grader.invoke({"question": question, "answer": generation})
        if answer_score:=score.binary_score:
            return "useful"
        else:
            return "not_useful"
    else:
        return "not_grounded"
    


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
workflow.add_conditional_edges(GENERATION, grade_generation_grounded_in_documents_and_question, 
    {
    "useful": END,
    "not_useful": WEB_SEARCH,
    "not_grounded": GENERATION}
)
workflow.add_edge(WEB_SEARCH, GENERATION)
workflow.add_edge(GENERATION, END)
app=workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path="flow.png")