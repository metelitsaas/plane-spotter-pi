import os
from package.utils.logger import logger
from message_loader import MessageLoader


def main():

    # dump1090 environment
    dump1090_params = {
        'host': os.environ['DUMP1090_HOST'],
        'port': os.environ['DUMP1090_PORT']
    }

    # web-server environment
    webserver_params = {
        'host': os.environ['WEBSERVER_HOST'],
        'port': os.environ['WEBSERVER_PORT']
    }

    # Run message loader
    message_loader = MessageLoader(dump1090_params, webserver_params)
    message_loader.run()


if __name__ == '__main__':

    try:
        logger.info('Starting')
        main()

    except Exception as error:
        logger.exception(error)
        logger.critical('Critical exception')
