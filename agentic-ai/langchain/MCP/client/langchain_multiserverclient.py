from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
import asyncio
from mcp.client.stdio import  stdio_client
from mcp import ClientSession, StdioServerParameters
from langchain_mcp_adapters.tools import  load_mcp_tools
from langgraph.prebuilt import create_react_agent



llm = ChatOllama(model="qwen3:1.7b")

std_server_params=StdioServerParameters(
command="python",
args=["/Users/jinto/Desktop/Repositories/Personal/ai-project-lab/agentic-ai/langchain/MCP/servers/math_server.py"],
)

async def main():
    async with stdio_client(std_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            # tools=await session.list_tools()
            tools=await load_mcp_tools(session)
            print(tools)
            agent=create_react_agent(
                model=llm,
                tools=tools,
            )
            result=await agent.ainvoke({"messages":[HumanMessage(content="What is 2+2?")]})
            print(result["messages"][-1].content)
if __name__ == "__main__":
    asyncio.run(main())