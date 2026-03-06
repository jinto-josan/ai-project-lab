import datetime
from dotenv import load_dotenv
from langchain_core.output_parsers import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from schemas import AnswerQuestion

load_dotenv()

llm= ChatOllama(model="qwen3:1.7b", temperature=0)

parser_pydantic= PydanticToolsParser(pydantic_object=AnswerQuestion)
parser= JsonOutputToolsParser(return_id=True)

actor_prompt= ChatPromptTemplate.from_messages([
    ("system", """
    You are a expert researcher. Current time is {current_time}.
    1. {first_instruction}
    2. Reflect and critique your answer. Be severe to maximise improvement.
    3. Recommend search queries to find relevant information and improve your answer.
    """),
    MessagesPlaceholder(variable_name="messages"),
]).partial(current_time=datetime.datetime.now().isoformat())

first_responder_prompt_template= actor_prompt.partial(first_instruction="Provide a detailed 250 word answer to the question")

first_response_chain= first_responder_prompt_template | llm.bind_tools(
    tools=[AnswerQuestion], tool_choice="AnswerQuestion"
)

if __name__=="__main__":
    human_message= HumanMessage(content="Write about AI powered SOC/autonomous soc problem domain," 
    "list startups that do that and raise capital"
    )
    chain=(
        first_responder_prompt_template|llm.bind_tools(
            tools=[AnswerQuestion], tool_choice="AnswerQuestion"
        )|parser_pydantic
    )
    res=chain.invoke({"messages":[human_message]})
    print(res)