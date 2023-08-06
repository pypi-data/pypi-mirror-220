import requests
import json
import mutual

default_judge_message_response = {
    "judge_message_id": None,
    "default_message": None,
    "unnatural_lang_message": None,
    "manipulation_message": None,
    "details": "Successful"
}

def get_judge_messages(limit=20, offset=0):
    url = f"https://api-agent.mutuai.io/api/judge_messages?limit={limit}&offset={offset}"
    # url = f"http://127.0.0.1:8000/api/judge_messages?limit={limit}&offset={offset}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_judge_message_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_judge_message_response

def get_judge_message(judge_message_id):
    url = f"https://api-agent.mutuai.io/api/judge_messages/{str(judge_message_id)}"
    # url = f"http://127.0.0.1:8000/api/judge_messages/{str(judge_message_id)}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    # response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    if response.status_code < 300:
        return response.json()
    else:
        default_judge_message_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_judge_message_response

def create_judge_message(
    judge_message_id,
    default_message=None,
    unnatural_lang_message=None,
    manipulation_message=None
):
    url = f"https://api-agent.mutuai.io/api/judge_messages"
    # url = f"http://127.0.0.1:8000/api/judge_messages"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "judge_message_id": judge_message_id,
        "default_message": default_message,
        "unnatural_lang_message": unnatural_lang_message,
        "manipulation_message": manipulation_message
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_judge_message_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {response.text}"
        return default_judge_message_response

def update_judge_message(
    judge_message_id,
    default_message=None,
    unnatural_lang_message=None,
    manipulation_message=None):

    url = f"https://api-agent.mutuai.io/api/judge_messages/{str(judge_message_id)}"
    # url = f"http://127.0.0.1:8000/api/judge_messages/{str(judge_message_id)}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "default_message": default_message,
        "unnatural_lang_message": unnatural_lang_message,
        "manipulation_message": manipulation_message
    }

    # remove keys with None value
    data = {k: v for k, v in data.items() if v is not None}
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_judge_message_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_judge_message_response
