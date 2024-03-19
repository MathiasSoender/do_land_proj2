from flask import Flask
from utils.db_connector import init_db
import urllib.parse

def create_app():
    app = Flask(__name__)
    init_db(app)
    return app
