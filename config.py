import configparser

config = configparser.ConfigParser()

# BOT_TOKEN = "6214808173:AAHmqWl1LL-9ytJ7T5MY9mTnfkvRADIOpv0"
# BOT_TOKEN = "7032292704:AAFChMlXgB41IlKs8CSOJxYBcB2C2buacpM"
BOT_TOKEN = '6214808173:AAHmqWl1LL-9ytJ7T5MY9mTnfkvRADIOpv0'

LOGS_PATH = f'logs.txt'
IAM_TOKEN_PATH = f'creds/iam_token.json'  # файл для хранения iam_token
FOLDER_ID_PATH = f'creds/folder_id.txt'  # файл для хранения folder_id
BOT_TOKEN_PATH = f'creds/bot_token.txt'  # файл для хранения bot_token

DB_FILE = 'db.db'
DB_TABLE_NAME = 'users'

MAX_USERS = 10  # лимит на общее количество пользователей
MAX_USER_TOKENS = 500

config['GPT'] = {
    'URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
    'TEMPERATURE': '0.6',
    'TOKENIZE_URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion',
    'MAX_ANSWER_GPT_TOKENS': '64'
}

config['LIMITS'] = {
    'MAX_MESSAGE_TOKENS': '50',
    'MAX_ANSWER_GPT_TOKENS': '64'
}

SYSTEM_PROMPT = {'role': 'system', 'text': 'Ты бот помощник в путешествиях. Пиши лаконично.'}
