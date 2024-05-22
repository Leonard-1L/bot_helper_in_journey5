import configparser

config = configparser.ConfigParser()

BOT_TOKEN = "7032292704:AAFChMlXgB41IlKs8CSOJxYBcB2C2buacpM"

LOGS_PATH = f'logs.txt'
DB_FILE = 'database.db'
DB_TABLE_NAME = 'users'
MAX_USERS = 5 #лимит на общее количество пользователей

config['GPT'] = {
    'URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
    'TEMPERATURE': '0.6',
    'TOKENIZE_URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion',
}

SYSTEM_PROMPT = [{'role': 'system', 'text': 'Ты веселый помощник по путешествиям.\n'
                                            'Отвечай интересно.\n'
                                            'Поддерживай диалог.'}]
