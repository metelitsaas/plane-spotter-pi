import socket
import time
from functools import wraps
from package.utils.logger import logger
from message import Message

BUFFER_SIZE = 100
RECONNECT_PERIOD = 1


def exception_handler(function):
    """
    Socket exception handler
    :param function: function to wrap
    :return: wrapped function
    """
    @wraps(function)
    def wrapper(self, *method_args, **method_kwargs):
        while True:

            try:
                return function(self, *method_args, **method_kwargs)

            except socket.error as error:
                logger.warning(error)
                self._disconnect()
                self._connect()

            except Exception as error:
                logger.exception(error)
                logger.warning('Unhandled exception')
                self._disconnect()
                raise

    return wrapper


class Receiver:
    """
    SBS-1 messages RTL-SDR receiver
    """
    def __init__(self, host: str, port: str):
        """
        Initialization
        :param host: host of receiver
        :param port: port of receiver
        """
        self._host = host
        self._port = int(port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect()

    def _connect(self) -> None:
        """
        Connect to socket
        """
        while True:

            try:
                logger.info(f"Connecting to {self._host}:{self._port}")
                self._socket.connect((self._host, self._port))
                logger.info(f"Connected to {self._host}:{self._port}")
                break

            except socket.error as error:
                logger.warning(error)
                logger.warning('Socket error, reconnecting')
                time.sleep(RECONNECT_PERIOD)

    def _disconnect(self) -> None:
        """
        Disconnect from socket
        """
        logger.info(f"Disconnecting from {self._host}:{self._port}")
        self._socket.close()

    @exception_handler
    def get_message(self) -> dict:
        """
        Get valid messages from receiver in loop
        :return: SBS-1 message
        """
        while True:
            response = self._socket.recv(BUFFER_SIZE)
            message = Message(response)

            if message.valid:
                yield message.get()
