import sqlite3
import logging

from config import DB_FILE, DB_TABLE_NAME, LOGS_PATH, MAX_USERS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOGS_PATH,
    filemode="a"
)


def create_database():  # функция, создающая базу данных
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {DB_TABLE_NAME} (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                total_tokens INTEGER,
                current_city TEXT)
            ''')
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        return None


def execute_query(sql_query, data=None,
                  db_path=DB_FILE):  # функция, которая выполняет sql-запрос и ничего не возвращает
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            if data:
                cursor.execute(sql_query, data)
            else:
                cursor.execute(sql_query)
            connection.commit()
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        return None


def execute_selection_query(sql_query, data=None,
                            db_path=DB_FILE):  # функция, которая выполняет sql-запрос и возвращает данные в формате списка с кортежами - [(...,), (...,), ...]
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            if data:
                cursor.execute(sql_query, data)
            else:
                cursor.execute(sql_query)
            rows = cursor.fetchall()
            connection.commit()
            return rows
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        return None


def add_new_user(user_id):  # добавляет нового пользователя, приниает в качестве аргумента id пользователя
    sql_query = f'INSERT INTO {DB_TABLE_NAME} (user_id, total_tokens, current_city) VALUES (?, ?, ?)'
    execute_query(sql_query, (user_id, 0, None))


def update_tokens(user_id,
                  add_tokens):  # обновляет кол.-во потраченных токенов, add_tokens - кол.-во токенов, которое надо добавить к существующему
    sql_query = f'UPDATE {DB_TABLE_NAME} SET total_tokens = total_tokens + {add_tokens} WHERE user_id={user_id};'  # todo использовать после каждого подсчёта токенов в новом запросе
    execute_query(sql_query)


def delete_user(user_id):  # удаляет указанного пользователя по id
    sql = f'DELETE FROM {DB_TABLE_NAME} WHERE user_id={user_id};'
    execute_query(sql)


def get_tokens(
        user_id):  # возвращает общее кол.-во потраченных токенов todo использовать для проверок на исчерпание лимита токенов
    sql_query = f'SELECT total_tokens FROM {DB_TABLE_NAME} WHERE user_id={user_id}'
    data = execute_selection_query(sql_query)[0]
    if data != ():
        return data[0]
    else:
        return 0


def change_city(user_id,  # меняет текущий город
                new_city):  # лучше хранить город так, а не в переменной, чтобы не было сбоев
    sql_query = f'UPDATE {DB_TABLE_NAME} SET current_city = "{new_city}" WHERE user_id={user_id};'
    execute_query(sql_query)


def get_city(user_id):
    sql_query = f'SELECT current_city FROM {DB_TABLE_NAME} WHERE user_id={user_id}'
    data = execute_selection_query(sql_query)
    return data[0][0]


def is_limit_users():  # возвращает True или False
    result = execute_selection_query(f'SELECT DISTINCT user_id FROM {DB_TABLE_NAME}')
    count = 0
    for i in result:
        count += 1
    return count >= MAX_USERS


def is_user(user_id):  # возвращает 1, если пользователь существует или 0, если нет
    sql = f'SELECT EXISTS(SELECT * FROM {DB_TABLE_NAME} WHERE user_id={user_id})'
    return execute_selection_query(sql)[0][0]

# create_database()
# add_new_user(2)
# update_tokens(1, 69)
# print(get_tokens(1))
# change_city(1, 'Казань')
# print(get_city(2))
# print(is_user(1))
# print(is_limit_users())
