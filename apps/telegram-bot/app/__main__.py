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

        if answer is None:
            message = 'ERROR: Empty message'
            bot.send_message(call.message.chat.id, message)

        elif 'error' in answer:
            message = 'ERROR: Server error'
            bot.send_message(call.message.chat.id, message)

        else:
            message = f"""
            Last received message:
            ID: {answer['hex_id']}
            Call Sign: {answer['call_sign_nm']}
            Date/Time: {answer['creation_dttm']}
            """
            bot.send_message(call.message.chat.id, message)

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
