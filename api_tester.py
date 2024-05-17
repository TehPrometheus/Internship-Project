import requests
import json
def get_data(api_url, bearer_token, id_param):
    # Define the headers with bearer authentication
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    # Define the parameters with the ID
    params = {
        'ID': id_param
    }

    # Make the GET request
    response = requests.get(api_url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        # Handle unsuccessful request
        print(f'Error: {response.status_code}')
        return None

# Example usage
if __name__ == '__main__':
    api_url = 'https://api.pdfmonkey.io/api/v1/document_cards'  # Replace with the actual API URL
    bearer_token = 'CvA6RXzdWH8NQyNm2jkZ'  # Replace with your actual bearer token
    id_param = '1faaa543-40d8-446f-8b6a-2a5a9508b968'  # Replace with the actual ID parameter

    data = get_data(api_url, bearer_token, id_param)
    if data:
        print(json.dumps(data, indent=4, sort_keys=True))
