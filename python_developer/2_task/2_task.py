import os

import openai
import telegram
from telegram import Update, ForceReply
from dotenv import load_dotenv
from telegram.ext import ConversationHandler, Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sqlite3

load_dotenv()


TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PASSWORD = "4321"

bot = telegram.Bot(token=TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY
model_engine = "text-davinci-003"


def create_database():
    connection = sqlite3.connect("message_history.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        username TEXT,
                        message_id INTEGER,
                        date TEXT,
                        text TEXT)''')
    connection.commit()
    connection.close()

create_database()

def save_message(user_id, username, message_id, date, text):
    connection = sqlite3.connect("message_history.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (user_id, username, message_id, date, text) VALUES (?, ?, ?, ?, ?)",
                   (user_id, username, message_id, date, text))
    connection.commit()
    connection.close()

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Приветствую!\n\nВведите пароль:',
                              reply_markup=ForceReply())


def password_check(update: Update, context: CallbackContext):
    user_input = update.message.text

    if user_input == PASSWORD:
        update.message.reply_text('Пароль верный. Приятного пользования.')
    else:
        update.message.reply_text('Пароль неверный. Попробуйте еще раз.',
                                  reply_markup=ForceReply())

def respond(update, context):

    message_text = update.message.text
    save_message(update.message.from_user.id, update.message.from_user.username, update.message.message_id, update.message.date, update.message.text)

    response = openai.Completion.create(
        model=model_engine,
        prompt=message_text,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    update.message.reply_text(response.choices[0].text)
    # bot_username = bot_answer.from_user.username
    # bot_user_id = bot_answer.from_user.id
    # save_message(bot_user_id, bot_username, bot_answer.message_id, bot_answer.date, bot_answer)
    save_message("Bot", "Bot", update.message.message_id,
                 update.message.date, response.choices[0].text)

def main():


    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.reply, password_check))

    dispatcher.add_handler(telegram.ext.MessageHandler(Filters.text & ~Filters.command, respond))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
