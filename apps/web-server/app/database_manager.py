import time
import datetime
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from package.utils.logger import logger
from package.database.message_id_seq import MessageIdSeq
from package.database.message import Message

RECONNECT_PERIOD = 1


def transaction_handler(function):
    """
    Transaction exception handler
    :param function: function to wrap
    :return: wrapped function
    """
    @wraps(function)
    def wrapper(self, *method_args, **method_kwargs):
        while True:

            try:
                result = function(self, *method_args, **method_kwargs)
                self._session.commit()

                return result

            except OperationalError as exception:
                logger.warning(exception)
                logger.warning('Rolling back transaction')
                self._session.rollback()

                time.sleep(RECONNECT_PERIOD)

            except (SQLAlchemyError, ValueError, TypeError) as exception:
                logger.exception(exception)
                logger.warning('Rolling back transaction')
                self._session.rollback()

                break

    return wrapper


class DatabaseManager:
    """
    Handles database data exchange
    """
    def __init__(self, params: dict):
        """
        Initialization
        :param params: database parameters
        """
        self._engine = create_engine('postgresql+psycopg2://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % {
            'user': params['user'],
            'password': params['password'],
            'host': params['host'],
            'port': params['port'],
            'db': params['db']
        })
        self._session = sessionmaker(bind=self._engine)()

    @transaction_handler
    def load_message(self, message: dict) -> int:
        """
        Create new message_id and load row to message table
        :param message: message
        :return: message_id of created message
        """
        message_id = self._create_message_id_seq()

        self._insert_message(message_id, message)

        return message_id

    def _create_message_id_seq(self) -> int:
        """
        Create new message_id_seq
        :return: message_id
        """
        return self._session.execute(MessageIdSeq)

    def _insert_message(self, message_id: int, row: dict) -> None:
        """
        Insert message row into message table
        :param message_id: generated message_id
        :param row: message row
        """
        message_row = Message(
            message_id,
            row['message_type'],
            row['transmission_type'],
            row['session_id'],
            row['aircraft_id'],
            row['hex_id'],
            row['flight_id'],
            row['call_sign_nm'],
            row['altitude_value'],
            row['ground_speed_value'],
            row['track_value'],
            row['latitude_value'],
            row['longitude_value'],
            row['vertical_rate'],
            row['squawk_value'],
            row['alert_flg'],
            row['emergency_flg'],
            row['spi_flg'],
            row['is_on_ground_flg'],
            row['generation_dttm'],
            row['received_dttm'],
            datetime.datetime.now()
        )
        self._session.add(message_row)
