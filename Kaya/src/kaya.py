import os
import time
import requests
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv
import asyncio
load_dotenv("C:/Users/tangu/Documents/GitHub Repositories/Internship Project/Kaya/.env")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

class Kaya:
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
        for event in stream:
           if event.event == "thread.message.delta":
              token = event.data.delta.content[0].text.value
              asyncio.run(msg.stream_token(token))
              print(event.data.delta.content[0].text.value, end="", flush=True)
           if event.event == "thread.run.requires_action":
              print("Kaya requires action")
              self.run_id = event.data.id
              self.handle_requires_action(event.data)

        asyncio.run(msg.send())

    def handle_requires_action(self, data):
      tool_outputs = []
        
      for tool in data.required_action.submit_tool_outputs.tool_calls:
        # TODO: start here. We want to pass each function name and its arguments to the Workato delegator recipe
        if tool.function.name == "get_current_weather":
          tool_outputs.append({"tool_call_id": tool.id, "output": "25 Celsius"})
      
      self.submit_tool_outputs(tool_outputs)

    def submit_tool_outputs(self,tool_outputs):
        msg = cl.Message(content="")
        with self.client.beta.threads.runs.submit_tool_outputs_stream(
        thread_id=self.thread_id,
        run_id=self.run_id,
        tool_outputs=tool_outputs,
      ) as stream:
            for text in stream.text_deltas:
                asyncio.run(msg.stream_token(text))
        asyncio.run(msg.send())
        

    def __run_thread(self):
        run = self.client.beta.threads.runs.create(thread_id = self.thread_id, assistant_id = ASSISTANT_ID)
        run_status = run.status
        
        max_loop_duration = 60
        timeout = False
        start_time = time.time()

        while run_status != "completed" or timeout != True:
            # Wait for 1 second
            time.sleep(1)

            # Retrieve run status
            run_status = self.client.beta.threads.runs.retrieve(thread_id = self.thread_id, run_id = run.id).status

            # Kaya needs to call a function, notify the Workato recipe
            if(run_status == "requires_action"):
                print("Kaya needs function outputs")
                # TODO: Implement Workato API call

            # Update the timer
            timeout = time.time() - start_time <= max_loop_duration

        if run_status == "completed":
            return True
        else:
            return False
    

    