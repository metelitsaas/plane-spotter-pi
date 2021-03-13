from package.utils.functions import datetime_to_string
from flask import request, abort, make_response, jsonify
from api_1_0 import api
from api_1_0 import database_manager

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


@api.route('/')
def index():
    """
    API index response
    """
    return jsonify({'apiVersion': 'v1'})


@api.route('/sbs-message', methods=['POST'])
def load_message():
    """
    Load SBS-1 message to database
    """
    data = request.get_json()

    if 'message_type' not in data:
        abort(400)

    message_id = database_manager.load_message(data)

    return make_response(jsonify({'message_id': message_id}), 201)


@api.route('/status', methods=['GET'])
def get_status():
    """
    Get status of system
    """
    timestamp = database_manager.get_last_message()

    if timestamp:
        message = f"Last message received at {datetime_to_string(timestamp)}"
        return make_response(message, 200)

    message = "Can't find message in database"
    return make_response(message, 200)
