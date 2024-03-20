from flask import Blueprint
from handlers.metrics.metrics_handlers import *

metric_views = Blueprint("metric_views", __name__)

@metric_views.route('/<metric_id>', methods=["GET"])
def get_metric(metric_id):
    return get_metric_handler(metric_id)


@metric_views.route("/", methods=["POST"])
def create_metric():
    return create_metric_handler()
