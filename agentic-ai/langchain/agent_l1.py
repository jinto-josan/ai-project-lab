from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable


MAX_ITERATIONS = 10
MODEL="gpt-oss:20b"
TEMPERATURE=0


@tool
def get_product_price(product_name: str) -> str:
    """
     A tool that returns the price of a product based on its name.
    """
    prices = {
        "laptop": 999,
        "smartphone": 499,
        "headphones": 199
    }
    return prices.get(product_name.lower(), 0)

@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """
    A tool that takes in product price and discount tier, and returns the discounted price.
     Discount tiers can be "premium", "gold", or "silver"
    """
    discount_tiers = {
        "premium": 20,
        "gold": 15,
        "silver": 10
    }
    discount_percentage = discount_tiers.get(discount_tier, 0)
    discounted_price = price * (1 - discount_percentage / 100)
    return round(discounted_price, 2)

@traceable(name="agent_l1_run")
def run_agent(question: str):
    tools= [get_product_price, apply_discount]
    tools_dict= {tool.name: tool for tool in tools}
    llm = init_chat_model(model=f"ollama:{MODEL}", temperature=TEMPERATURE)
    llm_with_tools= llm.bind_tools(tools)
    messages = [
        SystemMessage(
            """
            You are a helpful assistant and has access to product catalog tool and discount tool.
            STRICT GUIDELINES:
            1. Dont assume any product prices, always use the get_product_price tool to fetch the price.
            2. Always use the apply_discount tool to calculate discounted prices, never do it using any math.
            3. If user doesnt specify a valid discount tier, ask for discount tier before providing discounted price. 
            4. Always apply discount after fetching the price, never before. 
            """
        ),
        HumanMessage(question)
    ]
    
    for _ in range(1,MAX_ITERATIONS):

        print(f"Iteration: {_}")
        ai_message = llm_with_tools.invoke(messages)

        tool_calls = ai_message.tool_calls
        if not tool_calls:
            print(f"Agent response: {ai_message.content}")
            return ai_message.content
        tool_call= tool_calls[0]
        tool_name= tool_call.get("name")
        tool_args= tool_call.get("args", {})
        tool_id= tool_call.get("id")
        print(f"Tool call: {tool_name} with args {tool_args}")
        tool_func= tools_dict.get(tool_name)
        if not tool_func:
            print(f"Tool {tool_name} not found")
            return "Error: Tool not found"
        observation=tool_func.invoke(tool_args)
        print(f"Tool observation: {observation}")
        messages.append(
            ToolMessage(
                content=observation, # so that at every call agents knows about preveious tool calls and observations
                tool_call_id=tool_id #this helps in tracing
            )
        )
    print("Max iterations reached without a final answer.")

if __name__ == "__main__":
    load_dotenv()
    question = "What is the price of laptop with and without gold discount?"
    print(run_agent(question))
                

        