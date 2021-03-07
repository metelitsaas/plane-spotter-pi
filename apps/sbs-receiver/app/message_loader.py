import json
import requests
import datetime
import time
from functools import wraps
from requests import ReadTimeout, ConnectionError, HTTPError
from package.utils.logger import logger
from receiver import Receiver

RECONNECT_PERIOD = 1


def exception_handler(function):
    """
    Request exception handler
    :param function: function to wrap
    :return: wrapped function
    """
    @wraps(function)
    def wrapper(self, *method_args, **method_kwargs):
        while True:

            try:
                return function(self, *method_args, **method_kwargs)

            except (ReadTimeout, ConnectionError, HTTPError) as error:
                logger.warning(error)
                time.sleep(RECONNECT_PERIOD)

            except Exception as error:
                logger.exception(error)
                logger.warning('Unhandled exception')
                raise

    return wrapper


class MessageLoader:
    """
    Loads SBS-1 messages to web-server
    """
    def __init__(self, receiver_params: dict, webserver_params: dict):
        """
        Initialization
        :param receiver_params: receiver connection parameters
        :param webserver_params: web-server connection parameters
        """
        self._receiver = Receiver(receiver_params['host'], receiver_params['port'])
        self._webserver_host = webserver_params['host']
        self._webserver_port = webserver_params['port']

    def run(self) -> None:
        """
        Gets messages from receiver and loads it to web-server by API
        """
        for message in self._receiver.get_message():
            logger.info(f"Received message from aircraft hex_id: {message['hex_ident']}")
            message_ser = json.dumps(message, default=self._datetime_handler)
            self._send_message(message_ser)

    @exception_handler
    def _send_message(self, message: str) -> None:
        """
        Post message at web-server endpoint
        :param message: serialized message
        """
        url = f"http://{self._webserver_host}:{self._webserver_port}/sbs-message"
        content = {'Content-Type': 'application/json'}

        response = requests.post(url, data=message, headers=content)
        response.raise_for_status()

    @staticmethod
    def _datetime_handler(value) -> str:
        """
        Wrap datatime values to ISO format
        :param value: value to check
        :return: wrapped value
        """
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        else:
            return str(value)
