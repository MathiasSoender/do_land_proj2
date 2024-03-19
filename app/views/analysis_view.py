from flask import Blueprint
from handlers.analysis_handlers import *

analysis_views = Blueprint("analysis_views", __name__)


@analysis_views.route("/", methods=["GET"])
def get_all_analysis():
    return get_all_analysis_handler()


@analysis_views.route("/<analysis_id>", methods=["GET"])
def get_analysis_metric_types(analysis_id):
    return get_analysis_metric_types_handler(analysis_id)


@analysis_views.route("/<analysis_id>/<metric_type>", methods=["GET"])
def get_analysis_metric_type_sum_and_count(analysis_id, metric_type):
    return get_analysis_metric_type_sum_and_count_handler(analysis_id, metric_type)
