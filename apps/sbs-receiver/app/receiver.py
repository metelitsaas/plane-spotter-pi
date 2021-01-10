import socket
import time
from utils.logger import logger
from message import Message

BUFFER_SIZE = 100
RECONNECT_PERIOD = 1


class Receiver:
    """
    SBS-1 messages RTL-SDR receiver
    """
    def __init__(self, host: str, port: str):
        """
        :param host: host of receiver
        :param port: port of receiver
        """
        self._host = host
        self._port = int(port)

    def get_message(self):
        """
        Get valid messages from receiver in loop, handle reconnect for socket errors
        :return: SBS-1 message
        """
        while True:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                logger.info(f'Connecting to {self._host}:{self._port}')
                s.connect((self._host, self._port))
                logger.info(f'Connected')

                while True:
                    response = s.recv(BUFFER_SIZE)

                    if response is b'':
                        raise ValueError

                    message = Message(response)
                    if message.valid:
                        yield message.get()

            except ValueError:
                logger.warn('Empty message, attempting to reconnect')

            except socket.error as error:
                logger.warn(error)

            finally:
                s.close()
                time.sleep(RECONNECT_PERIOD)
