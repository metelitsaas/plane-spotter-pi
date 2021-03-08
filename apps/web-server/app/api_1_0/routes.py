from flask import request, abort, make_response, jsonify
from api_1_0 import api
from api_1_0 import database_manager


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
