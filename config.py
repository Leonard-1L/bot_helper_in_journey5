import configparser

config = configparser.ConfigParser()

BOT_TOKEN = ""


LOGS_PATH = f'logs.txt'
IAM_TOKEN_PATH = f'creds/iam_token.json'  # файл для хранения iam_token
FOLDER_ID_PATH = f'creds/folder_id.txt'  # файл для хранения folder_id
BOT_TOKEN_PATH = f'creds/bot_token.txt'  # файл для хранения bot_token

DB_FILE = 'db.db'
DB_TABLE_NAME = 'users'

MAX_USERS = 10  # лимит на общее количество пользователей
MAX_USER_TOKENS = 1000

config['GPT'] = {
    'URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
    'TEMPERATURE': '0.6',
    'TOKENIZE_URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion',
    'MAX_ANSWER_GPT_TOKENS': '250'
}

config['LIMITS'] = {
    'MAX_MESSAGE_TOKENS': '50',
    'MAX_ANSWER_GPT_TOKENS': '350'
}

SYSTEM_PROMPT = {'role': 'system', 'text': 'Ты бот помощник в путешествиях. Пиши лаконично.'}
