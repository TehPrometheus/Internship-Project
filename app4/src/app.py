import requests
import os
from dotenv import load_dotenv
load_dotenv()

WORKATO_API_KEY = os.getenv("WORKATO_API_KEY")
def get_assistant_response(api_key, content:str):
    url = "https://apim.workato.com/geertv1/stage-tanguy-apis-v1/get-assistant-response"
    headers = {
        "API-Token": api_key,
        "Content-Type": "application/json"
    }
    params = {
        "role": "user",
        "content": content
    }
    print("started request")
    response = requests.get(url, headers=headers, params=params)
    print("ended request")
    
    return response.json()

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Error: Unable to parse response JSON")
    elif response.status_code == 401:
        print("Unauthorized: Invalid API token")
    elif response.status_code == 422:
        print("Processing error")
    elif response.status_code == 500:
        print("Server error")
    else:
        print("Unknown error:", response.status_code)
    return None

# Example usage
content = "What is the current temperature in Paris?"  # Example content
assistant_response = get_assistant_response(WORKATO_API_KEY, content)
if assistant_response:
    print("Assistant response:", assistant_response)
