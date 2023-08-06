import requests
import json
import mutual

default_judge_response = {
    "judge_id": None,
    "world_prompt" :None,
    "action_prompt" : None,
    "judge_convo_aware" : None,
    "judge" : None,
    "judgement_lens" : None,
    "created_by" : None,
    "total_tokens": None,
    "details" : "Failed"
}

def get_judges(limit=20, offset=0):
    url = f"https://api-agent.mutuai.io/api/judges?limit={limit}&offset={offset}"
    # url = f"http://127.0.0.1:8000/api/judges?limit={limit}&offset={offset}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_judge_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_judge_response

def get_judge(judge_id):
    url = f"https://api-agent.mutuai.io/api/judges/{str(judge_id)}"
    # url = f"http://127.0.0.1:8000/api/judges/{str(judge_id)}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    # response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    if response.status_code < 300:
        return response.json()
    else:
        default_judge_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_judge_response

def create_judge(
    judge_id,
    world_prompt=None,
    action_prompt=None,
    judge_convo_aware=None,
    judge=None,
    judgement_lens=None
):
    url = f"https://api-agent.mutuai.io/api/judges"
    # url = f"http://127.0.0.1:8000/api/judges"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "judge_id": judge_id,
        "world_prompt" :world_prompt,
        "action_prompt" : action_prompt,
        "judge_convo_aware" : judge_convo_aware,
        "judge" : judge,
        "judgement_lens" : judgement_lens,
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_judge_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {response.text}"
        return default_judge_response

def update_judge(
    judge_id,
    world_prompt=None,
    action_prompt=None,
    judge_convo_aware=None,
    judge=None,
    judgement_lens=None):

    url = f"https://api-agent.mutuai.io/api/judges/{str(judge_id)}"
    # url = f"http://127.0.0.1:8000/api/judges/{str(judge_id)}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "world_prompt" :world_prompt,
        "action_prompt" : action_prompt,
        "judge_convo_aware" : judge_convo_aware,
        "judge" : judge,
        "judgement_lens" : judgement_lens,
    }

    # remove keys with None value
    data = {k: v for k, v in data.items() if v is not None}
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_judge_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_judge_response
