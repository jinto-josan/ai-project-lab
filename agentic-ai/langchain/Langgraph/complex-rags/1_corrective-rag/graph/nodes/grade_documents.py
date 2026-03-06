from typing import Any, Dict
from graph.state import GraphState
from graph.chains.retriever_grader import GradeDocuments, retriever_grader

def grade_documents_node(state:GraphState)->Dict[str, Any]:
    question=state["question"]
    documents=state["documents"]
    filtered_documents=[]
    websearch=False
    for doc in documents:
        res:GradeDocuments=retriever_grader.invoke({"question": question, "documents": doc.page_content})
        if res.binary_score == "yes":
            filtered_documents.append(doc)
        else:
            websearch=True
            continue
    return {"documents": filtered_documents, "question": question}