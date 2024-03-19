from handlers.metrics_handlers import get_all_metrics_dict
from models.analysis_entity import AnalysisEntity
from error_handling.DoLand_exceptions import *
from utils.db_connector import mongo
from utils.responses import success_response

def get_all_analysis_handler():
    try:
        all_metrics_dict = get_all_metrics_dict()
        cursor = mongo.db.analysis.find({"status":"DONE"})
        all_analysis = []
        for document in cursor:
            analysis = AnalysisEntity(**document)
            analysis.join_with_metrics(all_metrics_dict)
            all_analysis.append(analysis.to_dict(exclude=["status"]))

        return success_response(data = all_analysis)

    except Exception as E:
        handle_generic_try_catch(E)


def get_analysis_metric_types_handler(analysis_id):
    try:
        types = get_analysis_metric_types(analysis_id)
        return success_response(data = types)
    except Exception as E:
        handle_generic_try_catch(E)


def get_analysis_metric_type_sum_and_count_handler(analysis_id, metric_type):
    try:
        summed_raw, coverage_count = get_analysis_metric_type_sum_and_count(
            analysis_id, metric_type
        )
        return success_response(data={
            "summed_metric_value": summed_raw,
            "coverage_entity_count" : coverage_count
        })

    except Exception as E:
        handle_generic_try_catch(E)


### UNEXPOSED IN API ###
def get_analysis_metric_types(analysis_id):
    check_if_analysis_exists(analysis_id)
    pipeline = [
        {"$match": {"external_id": analysis_id}},
        {"$unwind": "$analysis.basic"},
        {"$group": {"_id": "$analysis.basic.metric_type"}},
    ]
    unique_metric_types = mongo.db.analysis.aggregate(pipeline)
    return [t["_id"] for t in unique_metric_types]


def get_analysis_metric_type_sum_and_count(analysis_id, metric_type):
    analysis = check_if_analysis_exists(analysis_id)
    # A bit too difficult with pipelines
    summed_raw, coverage_count = analysis.get_metric_type_sum_and_count(metric_type)
    return summed_raw, coverage_count


# Used to check for existence, otherwise throws error.
def check_if_analysis_exists(analysis_id):
    analysis_doc = mongo.db.analysis.find_one({"external_id": analysis_id})
    if analysis_doc is None:
        raise DoLandNotFoundException(
            f"The analysis with id, {analysis_id}, was not found." +
            " Either it is not generated, or the id is bad."
        )

    analysis = AnalysisEntity(**analysis_doc)
    if analysis.status == "FAILED":
        raise DoLandInternalErrorException(
            f"The analysis with id, {analysis_id}, failed in generating."
        )
    return analysis
