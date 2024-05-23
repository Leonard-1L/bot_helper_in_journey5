import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton
import logging
from config import LOGS_PATH, BOT_TOKEN, MAX_USER_TOKENS
from database import create_database, add_new_user, update_tokens, change_city, is_user, is_limit_users, get_tokens, \
    get_city
from gpt import ask_gpt, count_gpt_tokens

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOGS_PATH,
    filemode="a"
)

bot = telebot.TeleBot(token=BOT_TOKEN)
create_database()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_limit_users():  # проверка на лимит пользователей
        bot.send_message(message.chat.id, f"К сожалению, у бота слишком много пользователей")
        return
    markup = InlineKeyboardMarkup()
    itembtn1 = InlineKeyboardButton(text="Начинаем!", callback_data='russ')
    markup.add(itembtn1)
    bot.send_message(message.chat.id,
                     f"Привет, {message.from_user.first_name}! Я бот такой-то..."  # todo дописать вступление
                     f"\nНачинаем?",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_callback1(call):
    if call.data:
        msg = bot.send_message(call.message.chat.id,
                               text="Отлично! Я бот, который помогает в путешествиях. Смогу подобрать куда сходить, рассказать про"
                                    "выбранную тобой достопримечательность. \n"
                                    "А теперь напиши город в котором ты сейчас находишься:")
        bot.register_next_step_handler(msg, user_add)
    else:
        logging.error("Callback не сработал в начале.")


def user_add(message: Message):
    if is_user(message.from_user.id) == 0:
        add_new_user(message.from_user.id, message.from_user.first_name)
        change_city(user_id=message.from_user.id, new_city=message.text)
        logging.info(
            f"{message.from_user.username} c id {message.from_user.id} из города {message.text} теперь с нами!")
    send_about_city(message)


def send_about_city(message: Message):
    change_city(message.from_user.id, message.text)
    if get_tokens(message.from_user.id) > MAX_USER_TOKENS:
        bot.send_message(message.from_user.id, "Увы, но у тебя закончились токены на ответ.")
        return

    gpt_bool, gpt_text, gpt_tokens = ask_gpt(f"Расскажи про город {message.text}. Его историю, экономику и население.")
    if gpt_bool:
        update_tokens(user_id=message.from_user.id, add_tokens=gpt_tokens)
        logging.info(
            f"{message.from_user.username} c id {message.from_user.id} получил ответ. Затраченные токены: {gpt_tokens}")

    else:
        logging.error(f'{message.from_user.username} c id {message.from_user.id} не смог получить ответ от нейросети')

    bot.send_message(message.from_user.id, gpt_text)
    send_categories(message)


def send_categories(message: Message):
    keyboard = ReplyKeyboardMarkup(row_width=2)
    button1 = KeyboardButton('Повеселиться')
    button2 = KeyboardButton('Посмотреть достопримечательности')
    button3 = KeyboardButton('Перекусить')
    button4 = KeyboardButton('Поспать')
    keyboard.add(button1, button2, button3, button4)
    bot.send_message(message.from_user.id, text=f"Выбери, что хочешь сделать в городе {message.text}",
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, callback=categories_answer)


def categories_answer(message: Message):
    if get_tokens(message.from_user.id > MAX_USER_TOKENS):
        bot.send_message(message.from_user.id, "Увы, но у тебя закончились токены на ответ.")
        return
    gpt_bool, gpt_text, gpt_tokens = ask_gpt(
        f'Расскажи, где можно погулять в городе {get_city(message.from_user.id)} чтобы {message.text}')
    if gpt_bool:
        update_tokens(user_id=message.from_user.id, add_tokens=gpt_tokens)
        logging.info(
            f"{message.from_user.username} c id {message.from_user.id} получил ответ {gpt_text}. Затраченные токены: {gpt_tokens}")

    else:
        logging.error(f'{message.from_user.username} c id {message.from_user.id} не смог получить ответ от нейросети')
    bot.send_message(message.from_user.id, gpt_text)


@bot.message_handler(commands=['help'])
def send_help(message: Message):
    bot.send_message(message.from_user.id, "текст помощи")
    logging.info(f"{message.from_user.username} c id {message.from_user.id} запросил помощь.")


@bot.message_handler()
def others_message(message):
    bot.send_message(message.from_user.id, "Отправь мне голосовое или текстовое сообщение, и я тебе отвечу")


if __name__ == "__main__":
    logging.info("Бот запущен")
    bot.polling(none_stop=True)
