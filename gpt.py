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
iam_token = 't1.9euelZqYm5zNnJCTlZGWipmaipidl-3rnpWampPNisrKl5qQysqPj86Uj83l8_cqOUJN-e8lcGgV_t3z92pnP0357yVwaBX-zef1656VmpfKjMuJys3Lx4mLy4qMyZab7_zF656VmpfKjMuJys3Lx4mLy4qMyZabveuelZqWj4-UyZuanJabz86Pns_Pz7XehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.8zZ29Asbh1NG8fv7u64gLAgImmre0FtNsrcYsFBLLTBloh9lG_I_3eqxD86TogkWyIDHVvt5n6_CkD5DxwkZCw'
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

