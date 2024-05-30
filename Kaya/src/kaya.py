#  This Python script contains a wrapper class called Kaia, our Keen Artificial Intelligence Assistant.
import os
import asyncio
import requests
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv("C:/Users/tangu/Documents/GitHub Repositories/Internship Project/Kaya/.env")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
WORKATO_API_KEY = os.getenv("WORKATO_API_KEY_CHAINLIT_CLIENT")
WORKATO_RECIPE_DELEGATOR_URL = os.getenv("WORKATO_RECIPE_DELEGATOR_URL")

class Kaia:
    def __init__(self):
        self.client = OpenAI()
        self.assistant = self.client.beta.assistants.retrieve(ASSISTANT_ID)
        print(f"The assistant with name {self.assistant.name} has been retrieved")
        
    def create_empty_thread(self):
        self.thread_id = self.client.beta.threads.create().id
        print(f"The thread with id {self.thread_id} has been created")

    def add_message_to_thread(self,user_message):
        self.client.beta.threads.messages.create(thread_id= self.thread_id, role = "user", content = user_message)

    def run_thread_and_stream(self):
        stream = self.client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=ASSISTANT_ID, stream = True)
        msg = cl.Message(content="")
        asyncio.run(msg.send())
        for event in stream:
           if event.event == "thread.message.delta":
              token = event.data.delta.content[0].text.value
              asyncio.run(msg.stream_token(token))
              # print(event.data.delta.content[0].text.value, end="", flush=True)
           if event.event == "thread.run.requires_action":
              print("\nKaya requires action...")
              self.run_id = event.data.id
              self.handle_requires_action(event.data)

        asyncio.run(msg.send())

    def handle_requires_action(self, data):
        tool_calls = []
        print("\nConstructing tool_calls for Workato...")

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            tool_calls.append({"id":tool.id,"function":{"name": tool.function.name,"arguments":tool.function.arguments}})

        print(f"\nSending tool_calls to Workato, it contains: {tool_calls}")

        headers = {
            "api-token": WORKATO_API_KEY,
            "Content-Type": "application/json"
        }
        body = {
            "tool_calls": tool_calls
        }
        response = requests.post(url = WORKATO_RECIPE_DELEGATOR_URL, headers = headers, json = body).json()

        print("\nWorkato response received")
        print(f"\nresponse contains: {response}")

        self.submit_tool_outputs(response["tool_outputs"])

    def submit_tool_outputs(self,tool_outputs):
        print("\nSubmitting Workato response to Kaya...")
        msg = cl.Message(content="")
        with self.client.beta.threads.runs.submit_tool_outputs_stream(
        thread_id=self.thread_id,
        run_id=self.run_id,
        tool_outputs=tool_outputs,
      ) as stream:
            for text in stream.text_deltas:
                asyncio.run(msg.stream_token(text))
        asyncio.run(msg.send())