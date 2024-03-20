import threading
from handlers.portfolio.helpers import handle_portfolio_upload
from utils.file_system_funcs import generate_random_id
from models.portfolio_entity import PortfolioEntity
from error_handling.DoLand_exceptions import *
from utils.responses import success_response
import flask
from utils.Matter_requester import matter_requester
import json


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

    except Exception as E:
        handle_generic_try_catch(E)



