import datetime

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


def datetime_to_string(timestamp: datetime.datetime) -> str:
    """
    Transform datatime to string
    :param timestamp: timestamp in datetime format
    :return: timestamp in string format
    """
    return timestamp.strftime(TIMESTAMP_FORMAT)
