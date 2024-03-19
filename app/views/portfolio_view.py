from flask import Blueprint
from handlers.portfolio_handlers import *


portfolio_views = Blueprint("portfolio_views", __name__)
# Route defined by requirements, perhaps better to have a route with /portfolio
@portfolio_views.route('/', methods=["POST"])
def post_portfolio():
    return post_portfolio_handler()


