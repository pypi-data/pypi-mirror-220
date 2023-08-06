import requests
import json
import mutual

def signup(password = None, email = None):
    url = "https://api-agent.mutuai.io/api/signup"
    # url = "http://127.0.0.1:8000/api/signup"
    data = {
        "password": password,
        "email": email
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code < 300:
        response_json = response.json()
        mutual.api_key = response_json.get('api_key') # save the api_key to config
        return response_json
    else:
        return {
            "email": None,
            "api_key": None,
            "details":f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        }


def login(password = None, email = None):
    url = "https://api-agent.mutuai.io/api/login"
    # url = "http://127.0.0.1:8000/api/login"
    data = {
        "password": password,
        "email": email
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code < 300:
        response_json = response.json()
        mutual.api_key = response_json.get('api_key') # save the api_key to config
        return response_json
    else:
        return {
            "email": None,
            "api_key": None,
            "details":f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        }