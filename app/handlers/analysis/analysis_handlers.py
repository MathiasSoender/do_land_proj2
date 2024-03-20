from handlers.analysis.helpers import *
from handlers.metrics.helpers import get_all_metrics_dict
from models.analysis_entity import AnalysisEntity
from error_handling.DoLand_exceptions import *
from utils.db_utils import mongo
from utils.responses import success_response


def get_all_analysis_handler():
    try:
        all_metrics_dict = get_all_metrics_dict()
        cursor = mongo.db.analysis.find({"status": "DONE"})
        all_analysis = []
        for document in cursor:
            analysis = AnalysisEntity(**document)
            analysis.join_with_metrics(all_metrics_dict)
            all_analysis.append(analysis.to_dict(exclude=["status"]))

        return success_response(data=all_analysis)

    except Exception as E:
        handle_generic_try_catch(E)


def get_analysis_metric_types_handler(analysis_id):
    try:
        check_if_analysis_exists(analysis_id)
        types = get_analysis_metric_types(analysis_id)
        return success_response(data=types)
    except Exception as E:
        handle_generic_try_catch(E)


def get_analysis_metric_type_sum_and_count_handler(analysis_id, metric_type):
    try:
        check_if_analysis_exists(analysis_id)
        coverage_count = get_analysis_metric_type_coverage_count(
            analysis_id, metric_type
        )
        raw_sum = get_analysis_metric_type_raw_sum(analysis_id, metric_type)
        return success_response(
            data={
                "summed_metric_value": raw_sum,
                "coverage_entity_count": coverage_count,
            }
        )

    except Exception as E:
        handle_generic_try_catch(E)
