import time
import datetime
from functools import wraps
from sqlalchemy import create_engine, desc, func, distinct, case, true
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
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
        self._engine = create_engine(
            'postgresql+psycopg2://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % {
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

    @transaction_handler
    def get_statistics(self) -> dict:
        """
        Get full statistics info
        :return: answer dict
        """
        try:
            answer = self._session.query(
                func.count(Message.message_id),
                func.count(distinct(Message.hex_id)),
                func.sum(
                    case(
                        [(Message.emergency_flg == true(), 1)],
                        else_=0
                    )
                )
            ).one()

            return {
                'message_cnt': answer[0],
                'hex_id_dist_cnt': answer[1],
                'emergency_cnt': answer[2]
            }

        except NoResultFound:
            logger.warning("Answer set it empty")

    @transaction_handler
    def get_last_message(self) -> dict:
        """
        Get last message info
        :return: answer dict
        """
        try:
            answer = self._session.query(
                Message.hex_id,
                Message.call_sign_nm,
                Message.creation_dttm
            ).order_by(desc(Message.creation_dttm)).first()

            return {
                'hex_id': answer[0],
                'call_sign_nm': answer[1],
                'creation_dttm': answer[2]
            }

        except NoResultFound:
            logger.warning("Answer set it empty")

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
            row.get('message_type'),
            row.get('transmission_type'),
            row.get('session_id'),
            row.get('aircraft_id'),
            row.get('hex_id'),
            row.get('flight_id'),
            row.get('call_sign_nm'),
            row.get('altitude_value'),
            row.get('ground_speed_value'),
            row.get('track_value'),
            row.get('latitude_value'),
            row.get('longitude_value'),
            row.get('vertical_rate'),
            row.get('squawk_value'),
            row.get('alert_flg'),
            row.get('emergency_flg'),
            row.get('spi_flg'),
            row.get('is_on_ground_flg'),
            row.get('generation_dttm'),
            row.get('received_dttm'),
            datetime.datetime.now()
        )
        self._session.add(message_row)
