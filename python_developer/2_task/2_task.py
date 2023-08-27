import os

import openai
import telegram
from telegram import Update, ForceReply
from dotenv import load_dotenv
from telegram.ext import ConversationHandler, Updater, CommandHandler, MessageHandler, Filters, CallbackContext

load_dotenv()


TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PASSWORD = "4321"

bot = telegram.Bot(token=TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY
model_engine = "text-davinci-003"


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


    response = openai.Completion.create(
        model=model_engine,
        prompt=message_text,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    update.message.reply_text(response.choices[0].text)

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
