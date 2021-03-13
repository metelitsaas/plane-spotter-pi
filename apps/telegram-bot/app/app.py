import os
import telebot
from package.utils.logger import logger
from functions import *


# Bot environment variable
api_token = os.environ['API_TOKEN']

# Bot configuration
bot = telebot.TeleBot(api_token)


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
        answer = get_status()
        bot.send_message(call.message.chat.id, answer)

    elif call.data == 'emergency':
        answer = get_emergency()
        bot.send_message(call.message.chat.id, answer)


if __name__ == '__main__':

    try:
        logger.info('Starting')
        bot.polling()

    except Exception as error:
        logger.exception(error)
        logger.critical('Critical exception')
