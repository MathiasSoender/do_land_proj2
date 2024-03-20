from flask import Flask
from utils.db_utils import init_db
from views.metrics_view import metric_views
from views.portfolio_view import portfolio_views
from views.analysis_view import analysis_views
from views.pdf_views import pdf_views
from error_handling.error_middleware import errors_middleware

def create_app():
    app = Flask(__name__)
    init_db(app)
    app.register_blueprint(metric_views, url_prefix='/metric')
    app.register_blueprint(portfolio_views)
    app.register_blueprint(analysis_views)
    app.register_blueprint(pdf_views)

    app.register_blueprint(errors_middleware)

    return app
