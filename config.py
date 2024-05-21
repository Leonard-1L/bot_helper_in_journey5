import configparser

config = configparser.ConfigParser()

BOT_TOKEN = "7032292704:AAFChMlXgB41IlKs8CSOJxYBcB2C2buacpM"

HOME_PATH = '~'
LOGS_PATH = f'{HOME_PATH}/logs.txt' #у меня здесь вылезает ошибка (Нияз)
DB_FILE = 'database.db'
DB_TABLE_NAME = 'users'

config['GPT'] = {
    'URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
    'TEMPERATURE': '0.6',
    'TOKENIZE_URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion',
}

SYSTEM_PROMPT = [{'role': 'system', 'text': 'Ты веселый помощник по путешествиям. '
                                            'Подробно рассказывай о достопримечательностях выбранного пользователем город '
                                            'Поддерживай диалог.'}]