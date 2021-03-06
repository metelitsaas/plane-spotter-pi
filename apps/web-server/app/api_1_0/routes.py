from flask import jsonify
from api_1_0 import api


@api.route('/')
def index():
    """
    API index response
    """
    return jsonify({'apiVersion': 'v1'})
