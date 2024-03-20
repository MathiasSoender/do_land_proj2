from utils.db_utils import mongo, mongoPipeBuilder
from error_handling.DoLand_exceptions import *
from models.analysis_entity import AnalysisEntity


def get_analysis_metric_types(analysis_id):

    pipe = (
        mongoPipeBuilder()
        .analysis_external_id_match(analysis_id)
        .analysis_unwind_basics()
        .analysis_group_by_basic_attr("metric_type")
    ).build()

    unique_metric_types = mongo.db.analysis.aggregate(pipe)
    return [t["_id"] for t in unique_metric_types]

def get_analysis_metric_type_coverage_count(analysis_id, metric_type):
    pipe = (
        mongoPipeBuilder()
        .analysis_external_id_match(analysis_id)
        .analysis_unwind_basics()
        .analysis_match_basic_metric_type(metric_type)
        .analysis_sum_attr_of_metric("coverage.entity_count")
    ).build()

    result = mongo.db.analysis.aggregate(pipe)
    return sum(res["sum"] for res in result)


def get_analysis_metric_type_raw_sum(analysis_id, metric_type):
    pipe = (
        mongoPipeBuilder()
        .analysis_external_id_match(analysis_id)
        .analysis_unwind_basics()
        .analysis_match_basic_metric_type(metric_type)
        .analysis_sum_attr_of_metric("metric_value.raw")
    ).build()

    result = mongo.db.analysis.aggregate(pipe)
    type_count = sum(res["sum"] for res in result)
    return type_count


# Used to check for existence, otherwise throws error.
def check_if_analysis_exists(analysis_id):
    analysis_doc = mongo.db.analysis.find_one({"external_id": analysis_id})
    if analysis_doc is None:
        raise DoLandNotFoundException(
            f"The analysis with id, {analysis_id}, was not found."
            + " Either it is not generated, or the id is bad."
        )

    analysis = AnalysisEntity(**analysis_doc)
    if analysis.status == "FAILED":
        raise DoLandInternalErrorException(
            f"The analysis with id, {analysis_id}, failed in generating."
        )
    return analysis
