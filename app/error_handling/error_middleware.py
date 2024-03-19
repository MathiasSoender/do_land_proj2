from flask import Blueprint, jsonify
from error_handling.DoLand_exceptions import *

errors_middleware = Blueprint('errors_middleware', __name__)

@errors_middleware.app_errorhandler(DoLandBaseException)
def handle_doland_not_found_error(error: DoLandBaseException):
    response = jsonify({
        "error": error.description, 
        "DoLandErrCode": error.DoLandErrCode
    })
    response.status_code = error.code
    return response

