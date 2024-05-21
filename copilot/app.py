import chainlit as cl
import os
import requests
from dotenv import load_dotenv
load_dotenv("C:/Users/tangu/Documents/GitHub Repositories/Internship Project/copilot/.env")
WORKATO_API_KEY = os.getenv("WORKATO_API_KEY_CHAINLIT_CLIENT")
WORKATO_API_ENDPOINT = os.getenv("WORKATO_API_ENDPOINT")

def MakeRequest(message: cl.Message):
    THREAD_ID = cl.user_session.get("thread_id")

    url = WORKATO_API_ENDPOINT
    headers = {
        "api-token": WORKATO_API_KEY,
        "Content-Type": "application/json"
    }
     
    params = {
        "thread_id": THREAD_ID,
        "content": message.content
    }

    response = requests.post(url=url, headers=headers, json=params)

    return response.json()

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("thread_id", "")

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()
    if cl.context.session.client_type == "copilot":
        print(f"\n>>>>> User says: {message.content}\n")
        response = MakeRequest(message)
        print(f"\n>>>>> Kaya says: {response}")
        cl.user_session.set("thread_id", response["thread_id"]) 
        msg.content = response["message"]
        await msg.update()
