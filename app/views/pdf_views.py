from flask import Blueprint
from handlers.pdf.pdf_handlers import *

pdf_views = Blueprint("pdf_views", __name__)


@pdf_views.route("/pdf/<analysis_id>", methods=["GET"])
def get_pdf(analysis_id):
    return get_pdf_handler(analysis_id)
