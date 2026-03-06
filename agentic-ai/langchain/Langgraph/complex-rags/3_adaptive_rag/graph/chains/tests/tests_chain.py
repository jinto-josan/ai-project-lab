from dotenv import load_dotenv
load_dotenv()
from graph.chains.retriever_grader import GradeDocuments, retriever_grader
from ingestion import retriever
from graph.chains.generation_chain import generation_chain
from graph.chains.hallucination_grader import GradeHallucination, hallucination_grader
from pprint import pprint
from graph.chains.router import RouteQuery, question_router


def test_retriever_grader_yes()->None:
    question="What is hallucination?"
    documents=retriever.invoke(question)
    doc_text=documents[1].page_content
    res:GradeDocuments=retriever_grader.invoke({"question": question, "documents": doc_text})
    assert res.binary_score == "yes"

def test_retriever_grader_no()->None:
    question="What is the capital of France?"
    documents=retriever.invoke(question)
    doc_text=documents[1].page_content
    res:GradeDocuments=retriever_grader.invoke({"question": question, "documents": doc_text})
    assert res.binary_score == "no"

def test_generation_chain()->None:
    question="What is hallucination?"
    documents=retriever.invoke(question)
    generation=generation_chain.invoke({"question": question, "context": documents})
    pprint(generation)

def test_hallucination_grader_yes()->None:
    question="What is hallucination?"
    documents=retriever.invoke(question)
    doc_text=documents[1].page_content
    generation=generation_chain.invoke({"question": question, "context": documents})
    res:GradeHallucination=hallucination_grader.invoke({"documents": doc_text, "generation": generation})
    assert res.binary_score == "yes"

def test_hallucination_grader_no()->None:
    question="What is hallucination?"
    documents=retriever.invoke(question)
    doc_text=documents[1].page_content
    res:GradeHallucination=hallucination_grader.invoke({"documents": doc_text, "generation": "The capital of France is Paris."})
    assert res.binary_score == "no"

def test_question_router_to_vector_store()->None:
    question="What is hallucination?"
    res:RouteQuery=question_router.invoke({"question": question})
    assert res.datasource == "vector_store"

def test_question_router_to_web_search()->None:
    question="What is the capital of France?"
    res:RouteQuery=question_router.invoke({"question": question})
    assert res.datasource == "web_search"