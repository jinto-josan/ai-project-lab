from typing import Literal

from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama


class RouteQuery(BaseModel):
    """Route the query to the appropriate chain"""
    datasource: Literal["vector_store", "web_search"]=Field(...,
    description="Given a query, decide whether to route it to the vector store or web search.")

llm=ChatOllama(model="qwen3:1.7b", temperature=0)
structured_llm_router=llm.with_structured_output(RouteQuery)

system_prompt= """
You are an expert at routing queries to web search or vector store.
Given a query, decide whether to route it to the vector store or web search.
The vector store contains information related to agents, prompts and adversial attacks.
Use vector store for queries related to these topics. else route it to the web search.
"""

router_prompt= ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", """
    {question}
    """),
])
question_router=router_prompt | structured_llm_router