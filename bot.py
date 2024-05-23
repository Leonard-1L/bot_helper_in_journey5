import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import logging
from config import LOGS_PATH, BOT_TOKEN
from database import create_database, add_new_user, update_tokens, change_city, is_user, is_limit_users
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
    if is_limit_users(): #проверка на лимит пользователей
        bot.send_message(message.chat.id, f"К сожалению, у бота слишком много пользователей")
        return
    markup = InlineKeyboardMarkup()
    itembtn1 = InlineKeyboardButton(text="Начинаем!", callback_data='russ')
    markup.add(itembtn1)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Начинаем?",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_callback(call):
    if call.data:
        msg = bot.send_message(call.message.chat.id,
                               text="Отлично! Я бот, который помогает в путешествиях. Смогу подобрать куда сходить, рассказать про"
                                    "выбранную тобой достопримечательность. \n"
                                    "А теперь напиши город в котором ты сейчас находишься:")
        bot.register_next_step_handler(msg, user_add)


def user_add(message: Message):
    if is_user(message.from_user.id) == 0: #бот каждый раз добавлял пользователя заново
        add_new_user(message.from_user.id, message.from_user.first_name) #так что вот проверка
    change_city(message.from_user.id, message.text)
    gpt_bool, gpt_text, gpt_tokens = ask_gpt(f"Расскажи про город {message.text}. Его историю, экономику и население.")
    if gpt_bool:
        update_tokens(user_id=message.from_user.id, add_tokens=gpt_tokens)
        logging.info(
            f"{message.from_user.username} c id {message.from_user.id} получил ответ {gpt_text}. Токены: {gpt_tokens}")
    else:
        logging.error(f'{message.from_user.username} c id {message.from_user.id} не смог получить ответ от нейросети')
    bot.send_message(message.from_user.id, gpt_text)

    # TODO: на этих кнопках падает бот!
    markup2 = InlineKeyboardMarkup()
    itembtn1 = InlineKeyboardButton(text="Поесть", callback_data='пользователь хочет поесть')
    itembtn2 = InlineKeyboardButton(text="Переночевать", callback_data='пользователь хочет переночевать')
    itembtn3 = InlineKeyboardButton(text="Посмотреть достопримечательности",
                                    callback_data='пользователь хочет посмотреть достопримечательности')
    itembtn4 = InlineKeyboardButton(text="Повеселиться", callback_data='пользователь хочет повеселиться')
    markup2.add(itembtn1, itembtn4, itembtn3, itembtn2)
    bot.send_message(message.chat.id, f"Выбери, что хочешь сделать в городе {message.text}",
                     reply_markup=markup2)


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
