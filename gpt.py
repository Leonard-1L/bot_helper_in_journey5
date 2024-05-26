import logging
import requests
from config import config, SYSTEM_PROMPT, LOGS_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOGS_PATH,
    filemode="a"
)

iam_token = ""  # t1.9euelZqXjJK...
folder_id = ""  # b1gpk...


def count_gpt_tokens(messages):
    url = config['GPT']['TOKENIZE_URL']
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/yandexgpt-lite",
        "messages": messages
    }
    try:
        return len(requests.post(url=url, json=data, headers=headers).json()['tokens'])
    except Exception as e:
        logging.error(e)
        return 0


def ask_gpt(messages):
    try:
        url = config['GPT']['URL']
        headers = {
            'Authorization': f'Bearer {iam_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'modelUri': f"gpt://{folder_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": int(config['LIMITS']['MAX_ANSWER_GPT_TOKENS'])
            },
            "messages": [SYSTEM_PROMPT, {'role': 'user', 'text': messages}]
        }

        response = requests.post(url, headers=headers, json=data)
        print(response.json())
        logging.info('GPT: request sent!')
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None

        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer

    except Exception as e:
        logging.error(e)
        return False, "Ошибка при обращении к GPT", None
