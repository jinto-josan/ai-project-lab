from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama

def GradeDocuments(BaseModel)->str:
    """Binary score for relevance check on retrieved documents"""
    binary_score: bool = Field(description="Documents are relevant to the question, yes or no  ")


structured_llm_grader= ChatOllama(model="qwen3:1.7b", temperature=0).with_structured_output(GradeDocuments)
system_prompt= """
You are a helpful assistant that grades the quality of the documents retrieved for a given question.
if the document contains keywords or semantic information that is relevant to the question, return yes, otherwise return no.
Give a binary score 'yes' or 'no' based on the relevance of the documents to the question.
"""
grade_prompt= ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", """
    Retrieved Documents: \n\n{documents}\n\n User Question: {question}
    """),
])
retriever_grader= grade_prompt | structured_llm_grader
