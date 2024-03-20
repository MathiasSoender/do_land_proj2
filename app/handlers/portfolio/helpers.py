from models.analysis_entity import AnalysisEntity
from utils.db_utils import mongo
from utils.Matter_requester import matter_requester
import time
from error_handling.DoLand_exceptions import *


def handle_portfolio_upload(external_id):
    try:
        analysis_json = wait_for_analysis(external_id)
        analysis = AnalysisEntity(**analysis_json)
        analysis.reduce_analysis()
    except Exception as E:
        analysis = AnalysisEntity.analysis_failed_placeholder(external_id)
    finally:
        if analysis is not None:
            mongo.db.analysis.insert_one(analysis.to_dict())


def wait_for_analysis(external_id):
    retries = 0
    while 200 > retries:
        res = matter_requester.get_analysis_results(external_id)
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 202:  # 202 => not ready yet.
            time.sleep(0.5)
            retries += 1
        else:
            raise MatterAPIException(
                f"Unknown status code when GET analysis, code: {res.status_code}"
            )

    raise MatterAPIException(f"GET analysis timed out, code: {res.status_code}")
