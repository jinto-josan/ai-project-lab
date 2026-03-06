from dotenv import load_dotenv
from typing import TypedDict,Annotated

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, BaseMessage

from chains import reflection_chain, generation_chain

load_dotenv()

class MessageGraphState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#Define nodes
REFLECT="reflect"
GENERATE="generate"

def generate_node(state:MessageGraphState)->MessageGraphState:
    return {"messages": generation_chain.invoke({"messages": state["messages"]})}

def reflect_node(state:MessageGraphState)->MessageGraphState:
    res= reflection_chain.invoke({"messages": state["messages"]})
    return {"messages": [HumanMessage(content=res.content)]}

builder=StateGraph(state_schema=MessageGraphState)
builder.add_node(REFLECT, reflect_node)
builder.add_node(GENERATE, generate_node)
builder.set_entry_point(GENERATE)




def should_continue(state:MessageGraphState)->str:
    if len(state["messages"]) > 6:
        return END
    return REFLECT

builder.add_conditional_edges(GENERATE, should_continue,{
    END:END,
    REFLECT:REFLECT,
})

builder.add_edge(REFLECT, GENERATE)

app=builder.compile()
app.get_graph().print_ascii()

if __name__=="__main__":
    print("Hello Reflection Agent")
    inputs=HumanMessage(content="""Make this tweet more viral:
    @LangChainAI
    - newly tool calling feature is underrated.
    After a long wait, we finally have a way to use tools in langchain.
    Made a video covering newest blog.
    """
    )
    res=app.invoke({"messages":[inputs]})