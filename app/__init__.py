from flask import Flask
from utils.db_utils import init_db
from views.metrics_view import metric_views
from views.portfolio_view import portfolio_views
from views.analysis_view import analysis_views
from views.pdf_views import pdf_views
from error_handling.error_middleware import errors_middleware
from flask_swagger_ui import get_swaggerui_blueprint

HOST = "0.0.0.0"
BASE_PORT = "80"

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')    
    init_db(app)
    app.register_blueprint(metric_views)
    app.register_blueprint(portfolio_views)
    app.register_blueprint(analysis_views)
    app.register_blueprint(pdf_views)
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Test application"},
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    app.register_blueprint(errors_middleware)
    print(app.root_path)


    return app
