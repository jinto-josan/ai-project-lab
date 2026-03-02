from dotenv import load_dotenv
from langsmith import traceable
import ollama


MAX_ITERATIONS = 10
MODEL="gpt-oss:20b"
TEMPERATURE=0


@traceable(run_type="tool")
def get_product_price(product: str) -> str:
    """
     A tool that returns the price of a product based on its name.
    """
    prices = {
        "laptop": 999,
        "smartphone": 499,
        "headphones": 199
    }
    return prices.get(product.lower(), 0)

@traceable(run_type="tool")
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



# This is for olama curl based stuff
# But ollama sdk supports passing as list of function name, but the docstring needs to be in google style doc string
# with description, args and return


tools_for_llm=[
    {
        "name": "get_product_price",
        "description": "A tool that returns the price of a product based on its name.",
        "parameters": {
            "type": "object",
            "properties": {
                "product": {
                    "type": "string",
                    "description": "Name of the product to fetch price for. The products available are laptop, smartphone and headphones."
                }
            },
            "required": ["product"]
        }
    },
    {
        "name": "apply_discount",
        "description": "A tool that takes in product price and discount tier, and returns the discounted price.",
        "parameters": {
            "type": "object",
            "properties": {
                "price": {
                    "type": "number",
                    "description": "Price of the product."
                },
                "discount_tier": {
                    "type": "string",
                    "description": "Discount tier to apply. The discount tiers can be 'premium', 'gold', or 'silver'."
                }
            },
            "required": ["price", "discount_tier"]
        }
    }
]

# This aux function is required to have llm traces, with langchain langsmith automatically traces this llm call
@traceable(name="Ollama chat", run_type="llm")
def ollama_chat(messages):
    #https://docs.ollama.com/capabilities/tool-calling#tool-calling
    return ollama.chat(model=MODEL, messages=messages, tools=tools_for_llm)

@traceable(name="agent_l1_run")
def run_agent(question: str):
    tools= [get_product_price, apply_discount]
    #tools_dict= {tool.name: tool for tool in tools} #this tool.name was by the decorator @tool

    tools_dict={
        "get_product_price": get_product_price,
        "apply_discount": apply_discount
    }



    messages = [
        { "role": "system", "content": (
            "You are a helpful assistant and has access to product catalog tool and discount tool."
            "STRICT GUIDELINES: You have to strictly follow the below guidelines while answering user queries and you have to use the tools when required by invoking them with the right arguments."
            "1. Dont assume any product prices, always use the get_product_price tool by passing product to fetch the price."
            "2. Always use the apply_discount tool by passing price and discount_tier to calculate discounted prices, never calculate using any math."
            "3. If user doesnt specify a valid discount tier, ask for discount tier before providing discounted price. "
            "4. Always apply discount after fetching the price, never before. " 
        )},
        { "role": "user", "content": question }
    ]
    
    for _ in range(1,MAX_ITERATIONS):

        print(f"Iteration: {_}")
        response = ollama_chat(messages)
        ai_message = response.message

        tool_calls = ai_message.tool_calls
        if not tool_calls:
            print(f"Agent response: {ai_message.content}")
            return ai_message.content
        
        tool_call= tool_calls[0]
        tool_name= tool_call.function.name
        tool_args= tool_call.function.arguments

        print(f"Tool call: {tool_name} with args {tool_args}")
        tool_func= tools_dict.get(tool_name)
        if not tool_func:
            print(f"Tool {tool_name} not found")
            return "Error: Tool not found"
        
        #observation=tool_func.invoke(tool_args)# no runnable stuff that we got from langchain
        observation=tool_func(**tool_args)
        
        print(f"Tool observation: {observation}")
        messages.append(
            { "role": "tool", 
             "content": str(observation)} # so that at every call agents knows about preveious tool calls and observations
              
        )
    print("Max iterations reached without a final answer.")

if __name__ == "__main__":
    load_dotenv()
    question = "What is the price of laptop after applying gold discount?"
    print(run_agent(question))
                

        