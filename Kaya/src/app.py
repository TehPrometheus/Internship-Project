import chainlit as cl
from kaya import Kaya
from kaya import EventHandler

# Initialize Kaya
kaya = Kaya()

@cl.on_chat_start
async def on_chat_start():
    global kaya
    # Create an empty thread
    kaya.create_empty_thread()
    cl.user_session.set("thread_id", kaya.thread_id)

@cl.on_message
async def on_message(message: cl.Message):
    global kaya
    # Enable the loader icon by passing an empty message
    msg = cl.Message(content="")
    await msg.send()
    
    # Fetch Kaya's response to the user message
    # kaya_response = kaya.get_response(message.content)


    # Update the empy msg object with Kaya's response
    # msg.content = kaya_response

    text_delta = kaya.PassDeltaToChainlit();
    for token in text_delta:
        await msg.stream_token(token)

    await msg.send()




















