from flask import make_response, jsonify
from api_1_0 import api


@api.errorhandler(400)
def bad_request(message):
    """
    Handling 400 status error
    :param message: error message
    :return: json error message
    """
    response = jsonify({'error': 'bad_request', 'message': message})
    status_code = 400
    return make_response(response, status_code)


@api.errorhandler(404)
def not_found(message):
    """
    Handling 404 status error
    :param message: error message
    :return: json error message
    """
    response = jsonify({'error': 'not_found', 'message': message})
    status_code = 404
    return make_response(response, status_code)
