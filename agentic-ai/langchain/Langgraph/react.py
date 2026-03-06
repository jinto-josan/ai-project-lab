from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_ollama import ChatOllama



load_dotenv()

@tool
def triple(num:float)-> float:
    """
    param num: a num to triple
    returns: triple of num
    """
    return float(num) *3

tools=[TavilySearch(max_results=1), triple]

llm = ChatOllama(model="qwen3:1.7b", temperature=0).bind_tools(tools) # function tool