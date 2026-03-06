from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence


class GradeAnswer(BaseModel):
    """Binary score for answer check on retrieved documents"""
    binary_score: bool = Field(description="Answer addresses the question correctly, yes or no  ")

llm=ChatOllama(model="qwen3:1.7b", temperature=0)
structured_llm_grader=llm.with_structured_output(GradeAnswer)

system_prompt= """
You are a grader assessing weather an answer addresses/resolves the question correctly.
Give a binary score 'yes' or 'no' based on the relevance of the documents to the question. 
Yes means the answer addresses/resolves the question correctly, no means it does not.
"""
answer_prompt= ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", """
    Question: \n\n{question}\n\n Answer : {answer}
    """),
])

answer_grader:RunnableSequence= answer_prompt | structured_llm_grader