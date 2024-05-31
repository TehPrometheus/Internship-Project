# This Python script is responsible for running the Chainlit Chatbot Application and Initializing Kaya.
# Kaya is a wrapper class that wraps around the OpenAI Assistant API.
# Messages from the chat are intercepted and handled by Kaia.
import chainlit as cl
from kaia import Kaia

# 1) Initialize Kaia
kaia = Kaia()

@cl.on_chat_start
async def on_chat_start():
    global kaia
    # 2) Create an empty thread
    kaia.create_empty_thread()

@cl.on_message
async def on_message(message: cl.Message):
    global kaia
    # 3) Enable the loader icon by passing an empty message
    msg = cl.Message(content="")
    await msg.send()
    
    # 4) Add the user message to the thread
    kaia.add_message_to_thread(message.content)

    # 5) Run the thread and stream the response
    kaia.run_thread_and_stream()





















