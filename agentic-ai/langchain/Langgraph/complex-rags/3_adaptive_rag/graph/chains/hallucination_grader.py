from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

llm=ChatOpenAI(model="gpt-4o-mini", temperature=0)
class GradeHallucination(BaseModel):
    """Binary score for hallucination check on retrieved documents"""
    binary_score: bool = Field(description="Answer is grounded in facts, yes or no  ")

structured_llm_grader=llm.with_structured_output(GradeHallucination)

system_prompt= """
You are a grader assessing weather an LLM geneeration is grounded in / supported by the retrieved documents.
Give a binary score 'yes' or 'no' based on the relevance of the documents to the question. Yes means the generation is grounded in the documents, no means it is not.
"""
hallucination_prompt= ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", """
    Set of facts: \n\n{documents}\n\n LLM generation : {generation}
    """),
])
hallucination_grader:RunnableSequence= hallucination_prompt | structured_llm_grader