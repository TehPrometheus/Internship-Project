import os
import json
import requests
from IPython.display import display
from dotenv import load_dotenv
load_dotenv()

def show_json(obj):
    display(json.loads(obj.model_dump_json()))


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