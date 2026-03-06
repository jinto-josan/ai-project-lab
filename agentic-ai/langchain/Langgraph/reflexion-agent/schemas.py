from pydantic import BaseModel, Field
from typing import List


class Reflection(BaseModel):
    missing:str = Field(description="Critique of ehat is missing")
    superfluous:str = Field(description="Critique of what is superfluous")

class AnswerQuestion(BaseModel):
    """Schema for the answer to the question"""
    answer:str = Field(description="~250 words answer to the question")
    reflection:Reflection = Field(description="Your self-reflection on the answer")
    search_queries:List[str] = Field(description="1-3 search queries for researching improvements to address the critique of your current answer")

class RevisedAnswer(AnswerQuestion):
    """Schema for the revised answer to the question"""
    references:List[str] = Field(description="List of references used to answer the question")