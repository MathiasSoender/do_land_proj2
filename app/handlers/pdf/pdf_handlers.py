import threading
from flask import send_file
from handlers.pdf.helpers import generate_df_for_pdf
from error_handling.DoLand_exceptions import *
from utils.file_system_funcs import *
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table


def get_pdf_handler(analysis_id):
    tmp_pdf_filepath = ""
    try:
        tmp_pdf_dir = get_temp_dir()
        ensure_dir_exists(tmp_pdf_dir)
        tmp_pdf_filepath = os.path.join(
            tmp_pdf_dir, generate_random_id() + ".pdf"
        )

        df = generate_df_for_pdf(analysis_id)

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

