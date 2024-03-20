import os
import random
import string
import time


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_temp_dir(context="pdfs"):
    return os.path.join(os.getcwd(), "tmp", context)

def cleanup_file(path):
    if os.path.isfile(path):
        os.remove(path)


def cleanup_file_wait(tmp_pdf_filepath):
    time.sleep(30)
    cleanup_file(tmp_pdf_filepath)


def generate_random_id():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
