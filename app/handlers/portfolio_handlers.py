import threading
from utils.file_system_funcs import generate_random_id
from models.analysis_entity import AnalysisEntity
from models.portfolio_entity import PortfolioEntity
from error_handling.DoLand_exceptions import *
from utils.db_connector import mongo
from utils.responses import success_response
import flask
from utils.Matter_requester import matter_requester
import json
import time


def post_portfolio_handler():
    try:
        new_portfolio_data = flask.request.json
        try:
            portfolio = PortfolioEntity(**new_portfolio_data)
        except TypeError as E:
            raise DoLandBadReqException(
                f"The provided input portfolio was not formatted correctly, err: {str(E)}"
            )

        sum_needed_fixing = portfolio.fix_sum()
        external_id = generate_random_id()
        matter_requester.post_portfolio(json.dumps(portfolio.to_dict()), external_id)

        threading.Thread(target=handle_portfolio_upload, args=(external_id,)).start()

        return success_response(
            message = f"Portfolio posted, analysis is being created." + 
            f"{' Missing weights were set automatically.' if sum_needed_fixing else ''}",
            data = {"analysis_id" : external_id}
        )
        # mongo.db.analysis.insert_one(metric.to_dict())

    except Exception as E:
        handle_generic_try_catch(E)






### UNEXPOSED IN API ###



def handle_portfolio_upload(external_id):
    try:
        analysis_json = wait_for_analysis(external_id)
        analysis = AnalysisEntity(**analysis_json)
        analysis.reduce_analysis()
    except Exception as E:
        analysis = AnalysisEntity.get_analysis_failed_placeholder(external_id)
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
