from graph.graph import app
from dotenv import load_dotenv
load_dotenv()


if __name__=="__main__":
    print("Hello Agentic RAG")
    res=app.invoke({"question": "What is hallucination?"})
    print(res["generation"])