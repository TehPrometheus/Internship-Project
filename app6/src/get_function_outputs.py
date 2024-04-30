import requests
import asyncio

input = {'tool_calls': [{'Tool call ID': 'call_WKIk3G7c0HWOTxA5lFdW6Ncb','Function': {'Name': 'get_current_weather','Arguments': {"location":"Brussels"}}}],
         'base_url': 'https://apim.workato.com/geertv1/stage-tanguy-apis-v1/'}

def main(input):
    tool_outputs = []
    for call in input["tool_calls"]:
        params = {call['function']['arguments']}
        response = requests.post(url=f"{input['base_url']}{call['function']['name']}", params=params).text
        temp = {'tool_call_id': call['tool_call_id'], 'output': response}
        tool_outputs.append(temp)
    return {'tool_outputs': tool_outputs}


import requests
import json

def main(input):
    tool_outputs = []
    headers = {
        "api-token": input["WORKATO_API_KEY"],
        "Content-Type": "application/json"
    }