from dotenv import load_dotenv
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from react import llm,tools

load_dotenv()


SYSTEM_MESSAGE="You are helpful ai assistant that can use tools to answer"

def run_agent_reasoning(state:MessagesState)-> MessagesState:
    """Run agent reasoning code"""
    response=llm.invoke({"role":"system", "content":SYSTEM_MESSAGE}, *state["messages"])
    return {"messages":response}

tool_node = ToolNode(tools)