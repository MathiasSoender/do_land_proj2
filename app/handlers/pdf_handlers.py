import threading
from flask import send_file
from handlers.analysis_handlers import get_analysis_metric_types, get_analysis_metric_type_sum_and_count
from error_handling.DoLand_exceptions import *
from utils.db_connector import mongo
from utils.responses import success_response
from utils.file_system_funcs import *


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import pandas as pd
import time


def get_pdf_handler(analysis_id):
    tmp_pdf_filepath = ""
    try:
        tmp_pdf_dir = get_temp_dir()
        ensure_dir_exists(tmp_pdf_dir)
        tmp_pdf_filepath = os.path.join(
            tmp_pdf_dir, generate_random_id() + ".pdf"
        )

        df = generate_df_table(analysis_id)

        elements = [Table(df.values.tolist())]

        pdf = SimpleDocTemplate(tmp_pdf_filepath, pagesize=letter)
        pdf.build(elements)

        return send_file(
            tmp_pdf_filepath,
            mimetype="application/pdf",
            as_attachment=True,
        )

    except Exception as E:
        handle_generic_try_catch(E)
    finally:
        threading.Thread(target=cleanup_file_wait, args=(tmp_pdf_filepath,)).start()


# Wait a bit before del, otherwise the file is locked.
def cleanup_file_wait(tmp_pdf_filepath):
    time.sleep(30)
    cleanup_file(tmp_pdf_filepath)


def generate_df_table(analysis_id) -> pd.DataFrame:
    metric_types_used = get_analysis_metric_types(analysis_id)
    metric_sums = ["_METRIC_SUMS_"]
    metric_occurences = ["_METRIC_OCCURENCES_"]

    for metric_type in metric_types_used:
        metric_sum, metric_occurence = get_analysis_metric_type_sum_and_count(
            analysis_id,
            metric_type,
        )
        metric_sums.append(metric_sum)
        metric_occurences.append(metric_occurence)

    metric_types_used = ["_METRIC_TYPE_"] + metric_types_used
    data = {
        "Metric_Type": metric_types_used,
        "metric_sum": metric_sums,
        "metric_occurences": metric_occurences,
    }

    return pd.DataFrame(data)
