import joblib
import os

REPORT_PATH = "models/artifacts/classification_report.pkl"


def get_classification_report():

    if not os.path.exists(REPORT_PATH):
        return {
            "error": "Classification report not found"
        }

    report = joblib.load(REPORT_PATH)

    return report