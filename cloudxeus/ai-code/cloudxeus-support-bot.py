"""
 Require Azure search
 In AI Foundary language service playground, added qna and deployed it
 Deploy it as azure function with http trigger and key can be stored as environment variable
 Then create a client which call function with endpoint and key from function
 Also enable cors in azure function app
"""

import requests
from dotenv import load_dotenv
import os

load_dotenv()

endpoint="https://language-service-resource.cognitiveservices.azure.com/language/:query-knowledgebases?projectName=custom-qna&api-version=2021-10-01&deploymentName=production"
key=os.getenv("LANGUAGE_QNA_KEY")
headers={
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/json" 
}


def ask_question(question):
    data={
        "question": question,
        "top": 1,
    }
    response=requests.post(endpoint,headers=headers,json=data)
    result=response.json()
    answers=result.get("answers",[])
    if answers:
        # print(answers[0].get("confidenceScore",0.0))
        return answers[0]["answer"]
    else:
        return "I'm sorry, I don't have an answer for that question."

print(" Cloudxeus Support Bot")
while True:
    question=input("You: ")
    if question.lower() in ["exit", "quit"]:
        print("Cloudxeus: Goodbye!")
        break
    answer=ask_question(question)
    print("Cloudxeus: ",answer)




