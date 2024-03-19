# streamline responses, keep it simple for now.
from flask import jsonify

def success_response(message = None, data:dict = None, code = 200):
    response = {}
    if message is not None:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return jsonify(response), code


