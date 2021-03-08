import os
from flask import Blueprint
from database_manager import DatabaseManager

api = Blueprint('api_1_0', __name__)

# Database environment variables
params = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASS'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'db': os.environ['DB_NAME']
}
database_manager = DatabaseManager(params)

from api_1_0 import errors, routes
