import asyncio
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

async def main():
    llm=ChatOllama(model="qwen3:1.7b")
    prompt=ChatPromptTemplate.from_template("What is the capital of {country}?")
    chain=prompt | llm | StrOutputParser()
    print("Hello, World!")

if __name__ == "__main__":
    asyncio.run(main())