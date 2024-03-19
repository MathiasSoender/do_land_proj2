from flask_pymongo import PyMongo
import urllib.parse
from flask import Flask
from utils.secrets_fetch import *

mongo = PyMongo() # Keep outside of func to ensure availability for all files.

def init_db(app:Flask) -> None:
    username = urllib.parse.quote_plus(get_db_username())
    password = urllib.parse.quote_plus(get_db_password())
    app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@cluster0.kfps12u.mongodb.net/DoLand?retryWrites=true&w=majority&appName=Cluster0"
    mongo.init_app(app)

