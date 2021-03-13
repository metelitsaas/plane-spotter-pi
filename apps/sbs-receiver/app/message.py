import datetime
from typing import Optional
from package.utils.logger import logger

DECODE_TYPE = 'utf-8'
TIME_FORMAT = '%H:%M:%S.%f'
DATE_FORMAT = '%Y/%m/%d'


class Message:
    """
    SBS-1 message
    """
    def __init__(self, byte_message: bytes):
        """
        Initialization
        Parsing message values by position in list
        :param byte_message: received message in byte string
        """
        self._list_message = self._parse(byte_message)
        self.message_type = self._get_message_type(0)
        self.transmission_type = self._get_digit_value(1)
        self.session_id = self._get_digit_value(2)
        self.aircraft_id = self._get_digit_value(3)
        self.hex_id = self._get_exist_value(4)
        self.flight_id = self._get_digit_value(5)
        self.call_sign_nm = self._get_exist_value(10)
        self.altitude_value = self._get_digit_value(11)
        self.ground_speed_value = self._get_float_value(12)
        self.track_value = self._get_float_value(13)
        self.latitude_value = self._get_float_value(14)  # TODO: Check, always null
        self.longitude_value = self._get_float_value(15)  # TODO: Check, always null
        self.vertical_rate = self._get_float_value(16)
        self.squawk_value = self._get_digit_value(17)
        self.alert_flg = self._get_boolean_value(18)
        self.emergency_flg = self._get_boolean_value(19)
        self.spi_flg = self._get_boolean_value(20)
        self.is_on_ground_flg = self._get_boolean_value(21)
        self.generation_dttm = self._get_datetime_value(6, 7)
        self.received_dttm = self._get_datetime_value(8, 9)
        self.valid = self._check_validity()

    @staticmethod
    def _parse(byte_message: bytes) -> list:
        """
        Parse byte message to SBS-1 message format
        :param byte_message: received message in byte string
        :return: list of message fields
        """
        if byte_message != b'':

            splitted_message = byte_message \
                .decode(DECODE_TYPE) \
                .split('\n')

            for message in splitted_message:
                return message.split(",") if len(message.split(",")) == 22 else []

        else:
            return []

    def _get_message_type(self, position: int) -> Optional[str]:
        """
        Validate message_type value
        :param position: position of value in list
        :return: validated value
        """
        if len(self._list_message) > position:

            if len(self._list_message[position]) == 3:
                return self._list_message[position]

            return None

        return None

    def _get_digit_value(self, position: int) -> Optional[int]:
        """
        Validate digit value
        :param position: position of value in list
        :return: validated value
        """
        if len(self._list_message) > position:

            try:
                return int(self._list_message[position])

            except ValueError:
                return None

        return None

    def _get_float_value(self, position: int) -> Optional[float]:
        """
        Validate float value
        :param position: position of value in list
        :return: validated value
        """
        if len(self._list_message) > position:

            try:
                return float(self._list_message[position])

            except ValueError:
                return None

        return None

    def _get_exist_value(self, position: int) -> Optional[str]:
        """
        Validate existing value
        :param position: position of value in list
        :return: validated value
        """
        if len(self._list_message) > position:

            if self._list_message[position].strip() != '':
                return self._list_message[position].strip()

            return None

        return None

    def _get_boolean_value(self, position: int) -> Optional[bool]:
        """
        Validate boolean value
        :param position: position of value in list
        :return: validated value
        """
        if len(self._list_message) > position:

            if self._list_message[position].strip('\r') == '-1':
                return True
            if self._list_message[position].strip('\r') == '0':
                return False

            return None

        return None

    def _get_datetime_value(self, date_position: int,
                            time_position: int) -> Optional[datetime.datetime]:
        """
        Validate datetime value
        :param date_position: position of date value in list
        :param time_position: position of time value in list
        :return: validated datetime value
        """
        if len(self._list_message) > max(date_position, time_position):
            time = self._list_message[time_position]
            date = self._list_message[date_position]

            try:

                time_formatted = datetime.datetime.strptime(time, TIME_FORMAT).time()
                date_formatted = datetime.datetime.strptime(date, DATE_FORMAT).date()

                return datetime.datetime.combine(date_formatted, time_formatted)

            except ValueError:
                logger.info(f'Impossible to parse datetime: {date} {time}')
                return None

        return None

    def _check_validity(self) -> bool:
        """
        Check validity of the message
        :return: validity in boolean format
        """
        if self.message_type is not None:
            return True

        return False

    def get(self) -> dict:
        """
        Return SBS-1 formatted message
        :return: message in dictionary format
        """
        return {
            'message_type': self.message_type,
            'transmission_type': self.transmission_type,
            'session_id': self.session_id,
            'aircraft_id': self.aircraft_id,
            'hex_id': self.hex_id,
            'flight_id': self.flight_id,
            'call_sign_nm': self.call_sign_nm,
            'altitude_value': self.altitude_value,
            'ground_speed_value': self.ground_speed_value,
            'track_value': self.track_value,
            'latitude_value': self.latitude_value,
            'longitude_value': self.longitude_value,
            'vertical_rate': self.vertical_rate,
            'squawk_value': self.squawk_value,
            'alert_flg': self.alert_flg,
            'emergency_flg': self.emergency_flg,
            'spi_flg': self.spi_flg,
            'is_on_ground_flg': self.is_on_ground_flg,
            'generation_dttm': self.generation_dttm,
            'received_dttm': self.received_dttm
        }
