import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import logging
from config import LOGS_PATH, BOT_TOKEN
from database import create_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOGS_PATH,
    filemode="w"
)

bot = telebot.TeleBot(token=BOT_TOKEN)
create_database()#на всякий случай

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    itembtn = InlineKeyboardButton(text="Нажми меня!", callback_data='data')
    markup.add(itembtn)
    bot.send_message(message.chat.id, "Привет Нажми на кнопку ниже.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_callback(call):
    if call.data == 'data':
        bot.answer_callback_query(callback_query_id=call.id, text="Вы нажали на кнопку!")


@bot.message_handler(commands=['help'])
def send_help(message: Message):
    bot.send_message(message.from_user.id, "текст помощи")
    logging.info(f"{message.from_user.id} запросил помощь.")


@bot.message_handler(func=lambda: True)
def others_message(message):
    bot.send_message(message.from_user.id, "Отправь мне голосовое или текстовое сообщение, и я тебе отвечу")


if __name__ == "__main__":
    logging.info("Бот запущен")
    bot.polling(none_stop=True)
