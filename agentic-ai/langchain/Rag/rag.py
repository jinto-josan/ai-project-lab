import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

load_dotenv()

embeddings=OllamaEmbeddings(model="qwen3-embedding")
llm=ChatOllama(model="qwen3:1.7b")
vector_store=PineconeVectorStore(embedding=embeddings, index_name=os.environ["INDEX_NAME"])

retriever = vector_store.as_retriever( search_kwargs={"k": 3} )

prompt_template = ChatPromptTemplate.from_template(
    """
    Answer the question based on the following context:
    {context}
    Question: {question}
    Provide a detailed answer.
    """
)
                                                   
def format_docs(docs):
    """Formats the retrieved documents into a single string."""
    formatted_docs = []
    for doc in docs:
        formatted_docs.append(doc.page_content)
    return "\n\n".join(formatted_docs)

def retreiva_chain_without_lcel(question):
    """
    Retrieves relevant documents and generates an answer without using LCEL.
    Limitations:
    - Manual step by step execution
    - No built-in streaming support
    - No async support without additional code changes
    - Harder to compose with other chains or tools
    - More verbose and error-prone, and is difficult to trace
    """
    # Step 1: Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)
    
    # Step 2: Format the retrieved documents
    context = format_docs(retrieved_docs)
    
    # Step 3: Generate an answer using the LLM
    prompt = prompt_template.format_messages(context=context, question=question)

    #Step 4: Invoke the LLM to get the answer
    response = llm.invoke(prompt)
    
    #Step 5: Extract the content from the response
    return response.content

def retreiva_chain_with_lcel():
    """
    Create a retriever chain using LCEL for better composability, streaming, and async support.
    Returns a chain that is invoked with {"question" }
    Advantages of using LCEL:
    - Declarative and composable: easy to chain with pipe(|) operator
    - Built in streaming: chain.stream() works out of the box
    - Built in async support: chain.ainvoke() works out of the box
    - Batch processing: chain.batch() for multiple inputs
    - type safety: Better integration with langchain types and easier to debug and trace
    - Less code: More concise and readable
    - Reusable: Chain can be saved, shared & composed with other chains and tools
    - Better debugging: Langchain provides better observability tools
    """
    retrieval_chain = (
        # 1, 2 in above function
        RunnablePassthrough.assign( 
            #Basically it takes in an input dict of {"question": "What is pinecone?"} 
            # and allows us to use that input in the chain to create a new key called context 
            # so to prompt template we can pass in the question and context as variables.
            context= itemgetter("question") | retriever | format_docs
        )
        # 3, 4, 5 in above function
        |prompt_template 
        | llm 
        |StrOutputParser()
        ) 
    return retrieval_chain

if __name__ == "__main__":
    question = "What is pinecone?"
    answer = retreiva_chain_without_lcel(question)
    print("Answer:", answer)
    answer_with_lcel = retreiva_chain_with_lcel().invoke({"question": question})
    print("Answer with LCEL:", answer_with_lcel)
                                                  