import os
import sqlite3

import openai
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

load_dotenv()


class Settings:
    telegram_token = os.environ.get('TELEGRAM_TOKEN')
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    password = os.environ.get('PASSWORD')
    model_engine = "gpt-3.5-turbo"
    greeting_message = "Приветствую!\n\nВведите пароль:"
    correct_pass_msg = "Пароль верный. Приятного пользования."
    incorrect_pass_msg = "Пароль неверный. Попробуйте еще раз."
    db_name = "message_history.db"


class DB:
    def create_database(self):
        connection = sqlite3.connect(Settings().db_name)
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

    def save_message(self, user_id, username, message_id, date, text):
        connection = sqlite3.connect(Settings().db_name)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO messages (user_id, username, message_id, date, text) VALUES (?, ?, ?, ?, ?)",
                       (user_id, username, message_id, date, text))
        connection.commit()
        connection.close()


class Telegram:
    messages = []

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(Settings().greeting_message, reply_markup=ForceReply())

    def password_check(self, update: Update, context: CallbackContext):
        user_input = update.message.text

        if user_input == Settings().password:
            update.message.reply_text(Settings().correct_pass_msg)
        else:
            update.message.reply_text(Settings().incorrect_pass_msg, reply_markup=ForceReply())

    def respond(self, update, context):
        up_m = update.message
        message_text = up_m.text
        DB().save_message(up_m.from_user.id, up_m.from_user.username, up_m.message_id, up_m.date, up_m.text)
        self.messages.append({"role": "user", "content": message_text})

        response = openai.ChatCompletion.create(
            model=Settings().model_engine,
            messages=self.messages
        )
        response_msg = response.choices[0].message.content
        up_m.reply_text(response_msg)
        self.messages.append({"role": "assistant", "content": response_msg})
        DB().save_message("Bot", "Bot", up_m.message_id, up_m.date, response_msg)

    def clear_context(self, update, context):
        self.messages.clear()


def main():
    openai.api_key = Settings().openai_api_key
    DB().create_database()
    updater = Updater(token=Settings().telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', Telegram().start))
    dispatcher.add_handler(CommandHandler('clear_context', Telegram().clear_context))
    dispatcher.add_handler(MessageHandler(Filters.reply, Telegram().password_check))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, Telegram().respond))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
