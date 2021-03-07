import os
from package.utils.logger import logger
from receiver import Receiver


def main():

    # dump1090 environment
    dump1090_host = os.environ['DUMP1090_HOST']
    dump1090_port = os.environ['DUMP1090_PORT']

    # Set RTL-SDR receiver
    receiver = Receiver(dump1090_host, dump1090_port)

    # Get messages from receiver and send to broker
    for message in receiver.get_message():
        logger.info(f"Received message from aircraft hex_id: {message['hex_ident']}")


if __name__ == '__main__':

    try:
        logger.info('Starting')
        main()

    except Exception as error:
        logger.exception(error)
        logger.critical('Critical exception')
