import datetime
from abc import ABCMeta
from functools import wraps
from requests import ReadTimeout, HTTPError
from requests.exceptions import ConnectionError
from package.utils.logger import logger


class ApiLoader(metaclass=ABCMeta):
    """
    Abstract class of API loader
    """
    def __init__(self, params: dict):
        """
        Initialization
        :param params: web-server connection parameters
        """
        self._host = params['host']
        self._port = params['port']

    @staticmethod
    def _exception_handler(function):
        """
        Request exception handler
        :param function: function to wrap
        :return: wrapped function
        """
        @wraps(function)
        def wrapper(self, *method_args, **method_kwargs):

            try:
                return function(self, *method_args, **method_kwargs)

            except (ReadTimeout, ConnectionError, HTTPError) as error:
                logger.warning(error)

                return None

            except Exception as error:
                logger.exception(error)
                logger.warning('Unhandled exception')
                raise

        return wrapper

    @staticmethod
    def _datetime_handler(value) -> str:
        """
        Wrap datatime values to ISO format
        :param value: value to check
        :return: wrapped value
        """
        if isinstance(value, datetime.datetime):
            return value.isoformat()

        return str(value)
