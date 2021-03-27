import os
import telebot
from package.utils.logger import logger
from answers import generate_statistics_message, generate_last_message
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
    """
    Bot keyboard handler
    :param message: received message
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    key_status = telebot.types.InlineKeyboardButton(
        text='statistics', callback_data='statistics'
    )
    keyboard.add(key_status)

    key_status = telebot.types.InlineKeyboardButton(
        text='last message', callback_data='last_message'
    )
    keyboard.add(key_status)

    bot.send_message(message.chat.id, 'Choose action:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """
    Bot response logic
    :param call: response metadata
    """

    if call.data == 'statistics':
        answer = webserver_loader.get_statistics()
        message = generate_statistics_message(answer)
        bot.send_message(call.message.chat.id, message)

    elif call.data == 'last_message':
        answer = webserver_loader.get_last_message()
        message = generate_last_message(answer)
        bot.send_message(call.message.chat.id, message)


if __name__ == '__main__':

    try:
        logger.info('Starting')
        bot.polling()

    except Exception as error:
        logger.exception(error)
        logger.critical('Critical exception')
