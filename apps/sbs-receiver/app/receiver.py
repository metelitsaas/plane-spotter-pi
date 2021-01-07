import socket
import time
from utils.logger import logger
from message import Message

BUFFER_SIZE = 100
RECONNECT_PERIOD = 1


class Receiver:
    def __init__(self, host: str, port: str):
        self._host = host
        self._port = int(port)

    def get_message(self):

        while True:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                s.connect((self._host, self._port))
                logger.info(f'SBS-1. Connected to {self._host}:{self._port}')

                while True:
                    response = s.recv(BUFFER_SIZE)

                    if response is b'':
                        raise ValueError

                    message = Message(response)
                    if message.valid:
                        yield message.get()

            except ValueError:
                logger.warn('SBS-1. Empty message, attempting to reconnect')

            except socket.error as error:
                logger.warn(error)

            finally:
                logger.info(f'SBS-1. Closing connection to {self._host}:{self._port}')
                s.close()
                time.sleep(RECONNECT_PERIOD)
