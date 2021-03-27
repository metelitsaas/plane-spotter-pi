from functools import wraps


def check_answer(function):
    """
    incorrect answer handler
    :param function: function to wrap
    :return: wrapped function
    """
    @wraps(function)
    def wrapper(answer):

        if answer is None:
            return 'ERROR: Empty message'

        if 'error' in answer:
            return 'ERROR: Server error'

        return function(answer)

    return wrapper


@check_answer
def generate_statistics_message(answer: dict) -> str:
    """
    Generate statistics message
    :param answer: database response
    :return : message string
    """
    return f"""
            Statistics:
            All messages: {answer['message_cnt']}
            Unique planes: {answer['hex_id_dist_cnt']}
            Emergency messages: {answer['emergency_cnt']}
            """


@check_answer
def generate_last_message(answer: dict) -> str:
    """
    Generate last SBS-1 message
    :param answer: database response
    """
    return f"""
            Last message:
            Plane ID: {answer['hex_id']}
            Call sign: {answer['call_sign_nm']}
            UTC Timestamp: {answer['creation_dttm']}
            """
