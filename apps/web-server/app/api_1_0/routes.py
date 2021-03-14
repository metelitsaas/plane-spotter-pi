import json
from flask import request, abort, make_response, jsonify
from package.utils.functions import datetime_handler
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
    message = database_manager.get_last_message()

    if 'hex_id' not in message:
        abort(400)

    message_ser = json.dumps(message, default=datetime_handler)
    return make_response(message_ser, 200)
