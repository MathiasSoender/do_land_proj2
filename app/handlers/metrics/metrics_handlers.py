import flask
from error_handling.DoLand_exceptions import *
from utils.db_utils import mongo
from models.metrics_entity import MetricEntity
from utils.responses import success_response
import flask


def get_metric_handler(metric_id):
    try:
        metric_doc = mongo.db.metrics.find_one({'metric_id': metric_id})
        if metric_doc is None:
            raise DoLandNotFoundException(f"Metric with id {metric_id} not found.")

        metric = MetricEntity(**metric_doc)
        return success_response(data=metric.to_dict())

    except Exception as E:
        handle_generic_try_catch(E)


def create_metric_handler():
    try:
        new_metric_data = flask.request.json
        try:
            metric = MetricEntity(**new_metric_data) # Ensures that format is correct.
        except TypeError:
            raise DoLandBadReqException(f"The provided input was not formatted correctly.")

        mongo.db.metrics.insert_one(metric.to_dict())
        return success_response(message="Metric created", code=201)
    except Exception as E:
        handle_generic_try_catch(E)   

