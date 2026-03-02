import json
from dotenv import load_dotenv
from langsmith import traceable
import ollama
import inspect


MAX_ITERATIONS = 10
MODEL="qwen3:1.7b"
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

tools_dict={
        "get_product_price": get_product_price,
        "apply_discount": apply_discount
    }
def get_tool_descriptions():
    description = []
    for name, func in tools_dict.items():
        original_func= func.__wrapped__ if hasattr(func, "__wrapped__") else func # to get original function in case of decorated functions
        sig= inspect.signature(original_func)
        docstring= inspect.getdoc(original_func) or ""
        description.append(f"{name}{sig}: {docstring}")
    return "\n".join(description)
tool_descriptions=get_tool_descriptions()
tool_names=", ".join(tools_dict.keys())
react_prompt=f"""
 "STRICT GUIDELINES: You have to strictly follow the below guidelines while answering user queries and you have to use the tools when required by invoking them with the right arguments."
    "1. Dont assume any product prices, always use the get_product_price tool by passing product to fetch the price."
    "2. Always use the apply_discount tool by passing price and discount_tier to calculate discounted prices, never calculate using any math."
    "3. If user doesnt specify a valid discount tier, ask for discount tier before providing discounted price. "
    "4. Always apply discount after fetching the price, never before. " 

Answer the following questions as best you can. You have access to the following tools:
{tool_descriptions}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action in key value pair format if there are multiple arguments separate them by comma
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {{question}}
Thought:
"""


# This aux function is required to have llm traces, with langchain langsmith automatically traces this llm call
@traceable(name="Ollama chat", run_type="llm")
def ollama_chat(model,messages, options):
    #https://docs.ollama.com/capabilities/tool-calling#tool-calling
    return ollama.chat(model=model, messages=messages, options=options)

@traceable(name="agent_l1_run")
def run_agent(question: str):
    
    prompt= react_prompt.format(question=question)
    scratchpad=""
    for _ in range(1,MAX_ITERATIONS):
        full_prompt= prompt+ scratchpad
        print(f"Iteration: {_}")
        response = ollama_chat(model=MODEL, messages=[
            {"role": "user", "content": full_prompt}
            ],
                                options={"stop": ["\nObservation:"],# tells llm to stop generating text as soon as it generates "Observation:", this way we can parse the tool calls properly
                                         "temperature": TEMPERATURE})
        output = response.message.content

        # Parse the output to get the tool call and its arguments
        lines = output.split("\n")
        action_line = next((line for line in lines if line.startswith("Action:")), None)
        action_args_line = next((line for line in lines if line.startswith("Action Input:")), None)


        if not action_line or not action_args_line:
            print(f"Agent response: {output}")
            return output
        tool_name = action_line.split("Action:")[1].strip()
        tool_args = action_args_line.split("Action Input:")[1].strip() # assuming arguments are comma separated
       
        print(f"Tool call: {tool_name} with args {tool_args}")
        tool_func= tools_dict.get(tool_name)
        if not tool_func:
            print(f"Tool {tool_name} not found")
            return "Error: Tool not found"
        tool_args_dict=json.loads(tool_args)
        # ['{"product": "laptop"}'] -> {"product": "laptop"}

        
        observation=tool_func(**tool_args_dict)
        
        print(f"Tool observation: {observation}")
        scratchpad += f"\nThought: I should use the tool {tool_name} to get the answer\nAction: {tool_name}\nAction Input: {tool_args}\nObservation: {observation}\n"

    print("Max iterations reached without a final answer.")

if __name__ == "__main__":
    load_dotenv()
    question = "What is the price of laptop after applying gold discount?"
    print(run_agent(question))
                

        