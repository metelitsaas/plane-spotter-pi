import os
from flask import Flask
from plane_package.utils.logger import logger
from main import main as main_blueprint
from api_1_0 import api as api_1_0_blueprint


# Web-server environment
host = os.environ['HOST']
port = os.environ['PORT']

HOST = '0.0.0.0'
PORT = 5000

# Config Flask app
app = Flask(__name__)
app.register_blueprint(main_blueprint)
app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1')


if __name__ == '__main__':

    try:
        logger.info('Starting')
        app.run(host=HOST, port=PORT, debug=True, threaded=True)

    except Exception as error:
        logger.exception(error)
        logger.critical('Critical exception')
