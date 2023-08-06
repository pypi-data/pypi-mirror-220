import requests
import json
import mutual
import os
import platform

bot_default_response = {
            "bot_id": None,
            "bot_name": None,
            # "bot_org": None,
            "bot_chat_index": None,
            "prompt_id": None,
            "judge_id": None,
            "judge_message_id": None,
            "details": None
        }

def get_bots(limit=20, offset=0):
    url = f"https://api-agent.mutuai.io/api/bots?limit={limit}&offset={offset}"
    # url = f"http://127.0.0.1:8000/api/bots?limit={limit}&offset={offset}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response

def get_bot(bot_arg):
    url = f"https://api-agent.mutuai.io/api/bots/{str(bot_arg)}"
    # url = f"http://127.0.0.1:8000/api/bots/{str(bot_arg)}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    # response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response

def create_bot(bot_name=None, prompt=None, prompt_id = "default", judge_id="default", judge_message_id="default"):
    url = "https://api-agent.mutuai.io/api/bots"
    # url = "http://127.0.0.1:8000/api/bots"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "bot_name": bot_name,
        "prompt": prompt,
        "prompt_id": prompt_id or "default",
        "judge_id": judge_id or "default",
        "judge_message_id": judge_message_id or "default"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response

def update_bot(bot_id=None, bot_name=None, prompt_id=None, judge_id=None, judge_message_id=None):
    url = f"https://api-agent.mutuai.io/api/bots/{str(bot_id)}"
    # url = f"http://127.0.0.1:8000/api/bots/{str(bot_id)}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "bot_name": bot_name,
        "prompt_id": prompt_id,
        "judge_id": judge_id,
        "judge_message_id": judge_message_id
    }
    # remove keys with None value
    data = {k: v for k, v in data.items() if v is not None}
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response


class Bot:
    def __init__(self, api_key, bot_id=None, bot_name=None, prompt_id = "default", judge_id="default", judge_message_id="default"):
        self.api_key = api_key
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.prompt_id = prompt_id
        self.judge_id = judge_id
        self.judge_message_id = judge_message_id

        #
        self.flow = False

        self.default_stream_response = {
                        "error": None,
                        "status": "processing",
                        "content": None,
                        "data" : {
                            "bot_data": {
                                "bot_id": None,
                                "new_bot": False,
                                "new_bot_message": "Not a new bot.", 
                                "new_bot_user": False,
                                "new_bot_user_message": "Not a new bot_user.",
                            },
                            "prompt_data": {
                                "prompt_id": None,
                                "judge_id": None,
                                "judge_message_id": None,
                            },
                            "user_data": {
                                "username": None,
                                "tokens_used" : None
                            }
                        },
                    }

    def update_bot(self,  bot_name=None, prompt=None, prompt_id=None, judge_id=None, judge_message_id=None):
        url = f"https://api-agent.mutuai.io/api/bots/{str(self.bot_id)}"
        # url = f"http://127.0.0.1:8000/api/bots/{str(self.bot_id)}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "bot_name": bot_name,
            "prompt": prompt,
            "prompt_id": prompt_id,
            "judge_id" : judge_id,
            "judge_message_id" : judge_message_id
        }
        # remove keys with None value
        data = {k: v for k, v in data.items() if v is not None}
        response = requests.patch(url, data=json.dumps(data), headers=headers)
        if response.status_code < 300:
            return response.json()
        else:
            self.default_stream_response["content"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
            return self.default_stream_response

    def chat(self, content=None, username=None, prompt=None, multiplayer_memory = True, context_window = 2, flow=False, error_logs=False):
        url = "https://api-agent.mutuai.io/api/chat"
        # url = "http://127.0.0.1:8000/api/chat"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "content": content,
            "bot_id": str(self.bot_id),
            "bot_name": self.bot_name,
            "prompt": prompt,
            "username": username,
            "prompt_id": self.prompt_id,
            "judge_id": self.judge_id,
            "judge_message_id": self.judge_message_id,
            "multiplayer": multiplayer_memory,
            "context_window": context_window
        }

        if not content:
            print("Please add a message to the content.")
            return self.default_stream_response

        response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)


        if response.status_code < 300:
            is_new_bot = False
            is_new_user = False

            # add the newly created bot to the bot class
            print("\n", end="", flush=True)
            for line in response.iter_lines():
                if line:  # filter out keep-alive new lines
                    json_data = json.loads(line)
                    if not self.bot_id:
                        self.bot_id = json_data['data']['bot_data']['bot_id']
                    if json_data['error'] is not None and not error_logs:
                        continue
                    if json_data['data']['bot_data']['new_bot'] and not is_new_bot:
                        is_new_bot = True
                        print(f"Newly created bot! Here is your id: {json_data['data']['bot_data']['bot_id']}")
                    if json_data['data']['bot_data']['new_bot_user'] and not is_new_user:
                        is_new_user = True
                        print(f"New user {json_data['data']['user_data']['username']} created interacting with bot id: {json_data['data']['bot_data']['bot_id']}")
                    if json_data['content'] =='[close]':
                        continue
                    yield json_data

            if flow or self.flow:
                print("Type in clear into the input to clear the messages from the terminal...")
            while True:
                if flow or self.flow:
                    print("\n\n", end="", flush=True)
                    new_content = input("Please enter a new response or type exit to clear the screen or type clear to clear the screen: ")
                    if new_content.strip().lower() == "exit":
                        self.flow = False
                        break
                    elif new_content.strip().lower() == "clear":
                        # Detect the OS and run the clear command accordingly
                        if platform.system() == "Windows":
                            os.system('cls')
                        elif platform.system() == "Linux" or platform.system() == "Darwin":
                            os.system('clear')
                    else:
                        content = new_content
                        response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

                        if response.status_code < 300:
                            for line in response.iter_lines():
                                if line:  # filter out keep-alive new lines
                                    json_data = json.loads(line)
                                    if json_data['error'] is not None and not error_logs:
                                        continue
                                    if json_data['content'] =='[close]':
                                        continue
                                    yield json_data
        else:
            self.default_stream_response['content'] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
            print(f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}")
            return self.default_stream_response
