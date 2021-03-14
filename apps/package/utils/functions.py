import datetime

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


def datetime_handler(value) -> str:
    """
    Wrap datatime values to ISO format
    :param value: value to check
    :return: wrapped value
    """
    if isinstance(value, datetime.datetime):
        return value.strftime(TIMESTAMP_FORMAT)

    return str(value)
