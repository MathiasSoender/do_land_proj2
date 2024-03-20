from flask_pymongo import PyMongo
import urllib.parse
from flask import Flask
from utils.secrets_fetch import *

mongo = PyMongo()

def init_db(app:Flask) -> None:
    username = urllib.parse.quote_plus(get_db_username())
    password = urllib.parse.quote_plus(get_db_password())
    app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@cluster0.kfps12u.mongodb.net/DoLand?retryWrites=true&w=majority&appName=Cluster0"
    mongo.init_app(app)


class mongoPipeBuilder:

    def __init__(self):
        self.pipe = []

    def analysis_external_id_match(self, analysis_id):
        self.pipe.append({"$match": {"external_id": analysis_id}})
        return self

    def analysis_unwind_basics(self):
        self.pipe.append({"$unwind": "$analysis.basic"})
        return self

    def analysis_match_basic_metric_type(self, metric_type):
        self.pipe.append({"$match": {"analysis.basic.metric_type": metric_type}})
        return self

    def analysis_sum_attr_of_metric(self, attr_name):
        self.pipe.append(
            {
                "$group": {
                    "_id": "$_id",
                    "sum": {"$sum": f"$analysis.basic.{attr_name}"},
                }
            }
        )
        return self

    def analysis_group_by_basic_attr(self, attr_name):
        self.pipe.append({"$group": {"_id": f"$analysis.basic.{attr_name}"}})
        return self

    def build(self):
        return self.pipe
