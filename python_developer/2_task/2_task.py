import os

import openai
import telegram
from dotenv import load_dotenv
from telegram.ext import ConversationHandler, Updater

load_dotenv()


TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


bot = telegram.Bot(token=TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY
model_engine = "text-davinci-003"


def respond(update, context):

    message_text = update.message.text


    response = openai.Completion.create(
        model=model_engine,
        prompt=message_text,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7,
    )

    update.message.reply_text(response.choices[0].text)

def main():

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher


    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, respond))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
