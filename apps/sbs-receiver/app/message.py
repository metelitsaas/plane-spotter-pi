DECODE_TYPE = 'utf-8'


class Message:
    """
    SBS-1 message
    """
    def __init__(self, byte_message: bytes):
        """
        :param byte_message: received message in byte string
        """
        self._list_message = self._cleaner(byte_message)
        self.valid = self._check_valid()

    @staticmethod
    def _cleaner(byte_message: bytes):
        """
        Clean byte message to SBS-1 message format
        :param byte_message: received message in byte string
        :return: list of message fields
        """
        n_list = byte_message \
            .decode(DECODE_TYPE) \
            .split('\n')
        for n_item in n_list:
            return n_item.split(",") if len(n_item.split(",")) == 22 else None

    def _get_field(self, num_field: int):
        """
        Get message field from list by position
        :param num_field: number of SBS-1 message field
        :return: string of message field
        """
        return self._list_message[num_field] if self._list_message else ''

    def _check_valid(self):
        """
        Check validity of SBS-1 message, messages with empty aircraft hex id are invalid
        :return: validity
        """
        return True if self._get_field(4) not in ['000000', ''] else False

    def get(self):
        """
        Return SBS-1 formatted message
        :return: message in dictionary format
        """
        return {
            'message_type': self._get_field(0),
            'transmission_type': self._get_field(1),
            'session_id': self._get_field(2),
            'aircraft_id': self._get_field(3),
            'hex_ident': self._get_field(4),
            'flight_id': self._get_field(5),
            'date_message_gen': self._get_field(6),
            'time_message_gen': self._get_field(7),
            'date_message_log': self._get_field(8),
            'time_message_log': self._get_field(9),
            'call_sign': self._get_field(10),
            'altitude': self._get_field(11),
            'ground_speed': self._get_field(12),
            'track': self._get_field(13),
            'latitude': self._get_field(14),
            'longitude': self._get_field(15),
            'vertical_rate': self._get_field(16),
            'squawk': self._get_field(17),
            'alert': self._get_field(18),
            'emergency': self._get_field(19),
            'spi': self._get_field(20),
            'is_on_ground': self._get_field(21).strip('\r')
        }
