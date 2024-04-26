import chainlit as cl
import os
import requests
from dotenv import load_dotenv
load_dotenv("C:/Users/tangu/Documents/GitHub Repositories/Internship Project/app5/src/.env")

WORKATO_API_KEY = os.getenv("WORKATO_API_KEY_CHAINLIT_CLIENT")

def MakeRequest(message: cl.Message):
    THREAD_ID = cl.user_session.get("thread_id")

    url = "https://apim.workato.com/geertv1/stage-tanguy-apis-v1/get-assistant-response"
    headers = {
        "api-token": WORKATO_API_KEY,
        "Content-Type": "application/json"
    }
     
    params = {
        "thread_id": THREAD_ID,
        "content": message.content
    }

    response = requests.post(url=url, headers=headers, params=params)

    return response.json()

@cl.on_chat_start
def on_chat_start():
    cl.user_session.set("thread_id", "")

@cl.on_message
async def HandleUserMessage(message: cl.Message):

    response = MakeRequest(message)
    print(f"\n>>>> got the Workato API response as: \n{response}")
    cl.user_session.set("thread_id", response["thread_id"]) 
    # Send a response back to the user 
    await cl.Message(content = response['message']).send()
   