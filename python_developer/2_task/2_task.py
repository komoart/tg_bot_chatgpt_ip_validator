import os

import openai
import telegram
from dotenv import load_dotenv
from telegram.ext import ConversationHandler, CommandHandler, Updater, MessageHandler, Filters

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

# conv_handler = ConversationHandler(
#     entry_points=[CommandHandler('start', start)],
#     states={
#         PASSWORD: [MessageHandler(Filters.text, password)],
#         ACTION: [MessageHandler(Filters.text, action)]
#     },
#     fallbacks=[]
# )


def main():

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher


    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, respond))


    # updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()