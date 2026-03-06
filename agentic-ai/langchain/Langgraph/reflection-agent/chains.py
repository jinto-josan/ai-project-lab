from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama


reflection_prompt= ChatPromptTemplate.from_messages([
    ("system", """
    You are a viral twitter influencer.
    Generate critique recommendations for the user's tweet.
    Always provide detailed recommendations, including requests for length, viralitity, style tone, and content.
    """),
    MessagesPlaceholder(variable_name="messages"),
])

generation_prompt= ChatPromptTemplate.from_messages([
    ("system", """
    You are a twitter techie influencer assistant tasked with writing excellent twitter posts.
    Generate best possible tweet for the user's request.
    if user provides critique recommendations, respond with revised version of your previous attempts.
    """),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="messages"),
])
llm= ChatOllama(model="qwen3:1.7b", temperature=0)
reflection_chain= reflection_prompt | llm
generation_chain= generation_prompt | llm


