from flask import Blueprint

api = Blueprint('api_1_0', __name__)

from api_1_0 import errors, routes
