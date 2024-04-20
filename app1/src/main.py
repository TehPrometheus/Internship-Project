import openai
import time
import json
import os
import requests
# from utils.get_current_weather import get_current_weather
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_MODEL = os.getenv("ASSISTANT_MODEL")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Our first function call for Kaya: Getting the current weather
def get_current_weather(location):
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    try:
        url = "https://weatherapi-com.p.rapidapi.com/current.json"

        querystring = {"q": location}
        print(f"\n>>>> got the querystring as: {querystring}")
        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response_json = response.json()
        print(f"\n>>>> got the RAPID API response as: \n{response_json}")
        return response_json
    except Exception as e:
        raise e

# Create the tools list. This contains the functions Kaya will be able to call
tools_list = [{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Retrieve the latest weather conditions in a given city",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city you want to get the weather in"
                }
            },
            "required": ["location"]
        }
    }
}]

# Initialize OpenAI API client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Create Kaya, our OpenAI Assistant
# Currently, Kaya is already created. Her ASSISTANT_ID will be used instead.
# Kaya = client.beta.assistants.create(
#         name = "Kaya",
#         instructions =  """
#                         You are a weather assistant. Users ask you to tell me the weather in a given city. 
#                         The given city is required. You are given the get_current_weather function to get the current weather in the given city.
#                         As your first message, always greet the user in a friendly manner and tell them what you can do.
#                         """,
#         model = ASSISTANT_MODEL,
#         tools = tools_list)

# Create a Thread
thread = client.beta.threads.create()

# Add a message to the thread
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content= "Hello, can you tell me what the weather is in Paris?"
    )

# Run the thread
run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = ASSISTANT_ID,
    instructions = """Please greet the user in a friendly manner with your name, which is Kaya and tell them what you can do.""")

print(run.model_dump_json(indent = 4))

count = 0
max_count = 3

# Run the core loop. This while loop represents the conversation between the user and Kaya
while count < max_count:
    # wait for 10 seconds
    time.sleep(10)

    # retrieve the run status
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id)

    # print the run status
    print(run_status.model_dump_json(indent = 4))

    # If run is completed, get messages
    if run_status.status == "completed":
        print(f"STATUS >>>>> {run_status.status}")
        messages = client.beta.threads.messages.list(
            thread_id = thread.id)
    
        # Loop through messages and print content based on role
        for msg in messages.data:
            role = msg.role
            content = msg.content[0].text.value
            print(f"{role.capitalize()}: {content}")
    elif run_status.status == "requires_action":
        print(f"STATUS >>>>> {run_status.status}")
        required_actions = run_status.required_action.submit_tool_outputs.model_dump()
        print(required_actions)
        tool_outputs = []

        for action in required_actions["tool_calls"]:
            func_name = action['function']['name']
            arguments = json.loads(action['function']['arguments'])
            
            if func_name == "get_current_weather":
                output = get_current_weather(location=arguments['location'])
                output = json.dumps(output)
                tool_outputs.append({
                    "tool_call_id": action['id'],
                    "output": output
                })
            else:
                raise ValueError(f"Unknown function: {func_name}")
            
        print("STATUS >>>>> Submitting outputs back to the Assistant...")
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    else:
        print("\nWaiting for the assistant to complete...\n")
        print(f"STATUS >>>>> {run_status.status}\n")

    # Ensure that the while loop stops
    count += 1


