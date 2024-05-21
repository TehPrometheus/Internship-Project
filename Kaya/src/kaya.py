import os
import time
import requests
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
from dotenv import load_dotenv
load_dotenv("C:/Users/tangu/Documents/GitHub Repositories/Internship Project/Kaya/.env")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

class Kaya:
    def __init__(self):
        self.client = OpenAI()
        self.assistant = self.client.beta.assistants.retrieve(ASSISTANT_ID)
        print(f"The assistant with name {self.assistant.name} has been retrieved")
    
    def get_response(self,user_message):
        response = None

        self.__add_message_to_thread(user_message)
        
        # success = self.__run_thread()
        # if(success is not True):
        #     response = "Timeout Error: The thread took longer than 60s to complete!" 
        #     print(response)
        #     return response
        
        self.__run_thread_and_stream()
        response = "Stream done running"
        # response = self.client.beta.threads.messages.list(thread_id= self.thread_id, limit=1, order = "desc").data[0].content[0].text.value

        return response
        
    def create_empty_thread(self):
        self.thread_id = self.client.beta.threads.create().id
        print(f"The thread with id {self.thread_id} has been created")

    def __add_message_to_thread(self,user_message):
        self.client.beta.threads.messages.create(thread_id= self.thread_id, role = "user", content = user_message)

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
    
    def __run_thread_and_stream(self):
        with self.client.beta.threads.runs.stream(
            thread_id=self.thread_id,
            assistant_id=self.assistant.id,
            event_handler=EventHandler(),
            ) as stream:
                stream.until_done()

    
class EventHandler(AssistantEventHandler):
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)

  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)

  @override
  def on_event(self, event):
      # Retrieve events that are denoted with 'requires_action'
      # since these will have our tool_calls
      if event.event == 'thread.run.requires_action':
        run_id = event.data.id  # Retrieve the run ID from the event data
        self.handle_requires_action(event.data, run_id)

  def handle_requires_action(self, data, run_id):
    tool_outputs = []

    for tool in data.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "get_current_temperature":
            tool_outputs.append({"tool_call_id": tool.id, "output": "57"})
        elif tool.function.name == "get_rain_probability":
            tool_outputs.append({"tool_call_id": tool.id, "output": "0.06"})

    # Submit all tool_outputs at the same time
    self.submit_tool_outputs(tool_outputs, run_id)    
  
  def submit_tool_outputs(self, tool_outputs, run_id):
      # Use the submit_tool_outputs_stream helper
      with self.client.beta.threads.runs.submit_tool_outputs_stream(
        thread_id=self.current_run.thread_id,
        run_id=self.current_run.id,
        tool_outputs=tool_outputs,
        event_handler=EventHandler(),
      ) as stream:
        for text in stream.text_deltas:
          print(text, end="", flush=True)
        print()      

