from dotenv import load_dotenv
from langchain_core.messages import AIMessage,ToolMessage
from langgraph.graph import MessagesState, END, StateGraph, START
from langgraph.graph.state import Literal
from langgraph.prebuilt import ToolNode
from tool_executor import execute_tools
from chains import first_response_chain, revisor_chain
from schemas import AnswerQuestion, RevisedAnswer

load_dotenv()

MAX_ITERATIONS=3

def draft_node(state:MessagesState)->MessagesState:
    response=first_response_chain.invoke({"messages": state["messages"]})
    return {"messages": [response]}

def revise_node(state:MessagesState)->MessagesState:
    response=revisor_chain.invoke({"messages": state["messages"]})
    return {"messages": [response]}

def event_loop(state:MessagesState)->Literal["execute_tools",END]:

    count_tools=sum(isinstance(message, ToolMessage) for message in state["messages"])
    if count_tools < MAX_ITERATIONS:
        return "execute_tools"
    return END

builder=StateGraph(state_schema=MessagesState)
builder.add_node("draft", draft_node)
builder.add_node("revise", revise_node)
builder.add_node("execute_tools", execute_tools)


builder.add_edge(START, "draft")
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")
builder.add_conditional_edges(event_loop, {
    "execute_tools",
    END
})
app=builder.compile()
print(builder.get_graph().draw_mermaid())




if __name__=="__main__":
    print("Hello Reflexion Agent")

    res=app.invoke({"messages":[
        "role":"user",
        "content":"Write about AI powered SOC/autonomous soc problem domain," 
        "list startups that do that and raise capital"
    ]})
    last_message=res["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        print(last_message.tool_calls[0]["args"]["name"])