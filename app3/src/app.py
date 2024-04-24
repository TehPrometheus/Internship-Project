import requests
import os
from dotenv import load_dotenv
load_dotenv()

WORKATO_API_KEY = os.getenv("WORKATO_API_KEY")
def get_weather(api_key, location):
    url = "https://apim.workato.com/geertv1/stage-tanguy-apis-v1/get-weather"
    headers = {
        "API-Token": api_key,
        "Content-Type": "application/json"
    }
    params = {
        "location": location
    }
    response = requests.get(url, headers=headers, params=params)
    # return response.json()
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
location = "heusden-zolder"  # Example location
weather_data = get_weather(WORKATO_API_KEY, location)
if weather_data:
    print("Weather data:", weather_data)
