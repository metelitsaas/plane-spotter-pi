import os
import telebot
from requests.exceptions import ConnectionError
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


@bot.message_handler(commands=['statistics'])
def statistics(message):
    """
    Send statistics
    :param message: received message
    """
    answer = webserver_loader.get_statistics()
    response = f"""
            Statistics:
            All messages: {answer['message_cnt']}
            Unique planes: {answer['hex_id_dist_cnt']}
            Emergency messages: {answer['emergency_cnt']}
            """
    send_message(message.chat.id, response)


@bot.message_handler(commands=['last_message'])
def last_message(message):
    """
    Send last SBS-1 message
    :param message: received message
    """
    answer = webserver_loader.get_last_message()
    response = f"""
            Last message:
            Plane ID: {answer['hex_id']}
            Call sign: {answer['call_sign_nm']}
            UTC Timestamp: {answer['creation_dttm']}
            """
    send_message(message.chat.id, response)


def send_message(chat_id, message) -> None:
    """
    Send message chat with exception handling
    :param chat_id: telegram chat id
    :param message: message body
    """
    while True:
        try:
            bot.send_message(chat_id, message)
            break

        except ConnectionError:
            logger.warning('Connection error, trying again')


if __name__ == '__main__':

    try:
        logger.info('Starting')
        bot.polling()

    except Exception as error:
        logger.exception(error)
        logger.critical('Critical exception')
