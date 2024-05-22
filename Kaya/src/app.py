import chainlit as cl
from kaya import Kaya

# Initialize Kaya
kaya = Kaya()

@cl.on_chat_start
async def on_chat_start():
    global kaya
    # Create an empty thread
    kaya.create_empty_thread()

@cl.on_message
async def on_message(message: cl.Message):
    global kaya
    # Enable the loader icon by passing an empty message
    msg = cl.Message(content="")
    await msg.send()
    
    # Add the user message to the thread
    kaya.add_message_to_thread(message.content)

    # Run the thread and stream the response
    kaya.run_thread_and_stream()





















