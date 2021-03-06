from flask import jsonify
from main import main


@main.route('/')
def index():
    """
    Root index response
    """
    return 'plane-spotter-pi web-server'


@main.route('/health')
def get_health():
    """
    Check web-server liveness
    """
    return jsonify({'status': 'healthy'})
