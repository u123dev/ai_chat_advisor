import csv
import os

from settings import CUSTOM_QA_FILE


def init_file(filename=CUSTOM_QA_FILE):
    if not os.path.exists(filename):
        with open(filename, "a+", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            file.seek(0)
            if file.read(1) == '':
                writer.writerow(["Question", "Answer"])


def add_answer(question, result, filename=CUSTOM_QA_FILE):
    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([question.question, result])
        # print([question.question, result])
