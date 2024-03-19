from flask import Blueprint, jsonify, make_response
from models.portfolio_entity import PortfolioEntity
from error_handling.DoLand_exceptions import *
from utils.db_connector import mongo
from utils.responses import success_response
import flask
from utils.Matter_requester import matter_requester
import json
import random
import string


portfolio_views = Blueprint("portfolio_views", __name__)
# Route defined by requirements, perhaps better to have a route with /portfolio
@portfolio_views.route('/', methods=['POST'])
def post_portfolio():
    try:
        new_portfolio_data = flask.request.json
        try:
            portfolio = PortfolioEntity(**new_portfolio_data)
        except TypeError as E:
            raise DoLandBadReqException(
                f"The provided input portfolio was not formatted correctly, err: {str(E)}")

        sum_needed_fixing = portfolio.fix_sum()
        
        external_id =         
        matter_requester.post_portfolio(json.dumps(portfolio.to_dict()))

    except Exception as E:
        handle_generic_try_catch(E)


def generate_external_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
