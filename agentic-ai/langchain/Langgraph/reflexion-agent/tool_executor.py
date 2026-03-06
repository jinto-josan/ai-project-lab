from dotenv import load_dotenv
from langchain_core.tools import StructuredTool
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode
from schemas import  AnswerQuestion, RevisedAnswer

load_dotenv()


tavily_search_tool= TavilySearch(max_results=3)

def search_web_tool(search_queries:List[str])->str:
    """Search the web for information"""
    return tavily_search_tool.batch([{"query": query} for query in search_queries])

execute_tools=ToolNode(tools=[
    StructuredTool.from_function(
        search_web_tool,
        name=AnswerQuestion.__name__,
    ),
    StructuredTool.from_function(
        search_web_tool,
        name=RevisedAnswer.__name__,
    ),
])