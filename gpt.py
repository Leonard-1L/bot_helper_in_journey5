import logging
import requests
from config import config, SYSTEM_PROMPT, LOGS_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOGS_PATH,
    filemode="a"
)

# iam_token, folder_id =
iam_token = 't1.9euelZqNjJvOzInGnZXNks2KkZzPm-3rnpWampPNisrKl5qQysqPj86Uj83l8_cAUzxN-e8rRH5I_N3z90ABOk357ytEfkj8zef1656VmpzLys_OjJeYnc_Mi8nNnJPI7_zF656VmpzLys_OjJeYnc_Mi8nNnJPIveuelZqcz5OZjMmPncrKmc2YysnLlLXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.PFPYHCbsZ-2jmJ6zZS_k3IZQZ-WBqvzEAcWhpt0IR1ksXmdY2bA718wSre3q40jvqOfMwhbp_jXptZpvn3bgAg'
folder_id = 'b1gnl6btbg8ba5ub4odq'


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

