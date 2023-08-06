import requests
import json
import mutual

default_api_key_response = {
        "prev_api_key_name": None,
        "new_api_key_name": None,
        "api_key": None,
        "details": "Failed"
    }

def update_api_key(new_api_key_name):

    url = f"https://api-agent.mutuai.io/api/api_key"
    # url = f"http://127.0.0.1:8000/api/api_key"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "new_api_key_name" :new_api_key_name,
    }

    # remove keys with None value
    data = {k: v for k, v in data.items() if v is not None}
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        mutual.api_key = new_api_key_name
        return response.json()
    else:
        default_api_key_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_api_key_response