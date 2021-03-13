import os
import telebot
from package.utils.logger import logger
from webserver_loader import WebserverLoader


# Environment variables
api_token = os.environ['API_TOKEN']
webserver_params = {
    'host': os.environ['WEBSERVER_HOST'],
    'port': os.environ['WEBSERVER_PORT']
}

# Bot configuration
bot = telebot.TeleBot(api_token)

# Web-server API loader
webserver_loader = WebserverLoader(webserver_params)


@bot.message_handler(commands=['bot'])
def bot_handler(message):

    keyboard = telebot.types.InlineKeyboardMarkup()

    key_status = telebot.types.InlineKeyboardButton(text='status', callback_data='status')
    keyboard.add(key_status)

    key_emergency = telebot.types.InlineKeyboardButton(text='emergency', callback_data='emergency')
    keyboard.add(key_emergency)

    bot.send_message(message.chat.id, 'Choose action:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    if call.data == 'status':
        answer = webserver_loader.get_status()

        if answer:
            bot.send_message(call.message.chat.id, answer)

        else:
            bot.send_message(call.message.chat.id, 'Server error')

    elif call.data == 'emergency':
        answer = webserver_loader.get_emergency()
        bot.send_message(call.message.chat.id, answer)


if __name__ == '__main__':

    try:
        logger.info('Starting')
        bot.polling()

    except Exception as error:
        logger.exception(error)
        logger.critical('Critical exception')
