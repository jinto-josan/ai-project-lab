from dotenv import load_dotenv
from graph.chains.retriever_grader import GradeDocuments, retriever_grader
from ingestion import retriever
from graph.chains.generation_chain import generation_chain

load_dotenv()

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