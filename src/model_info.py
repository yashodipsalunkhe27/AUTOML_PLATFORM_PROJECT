import os
import joblib

MODEL_DIR = "models"

MODEL_NAME_PATH = os.path.join(
    MODEL_DIR,
    "model_name.pkl"
)

PROBLEM_TYPE_PATH = os.path.join(
    MODEL_DIR,
    "artifacts",
    "problem_type.pkl"
)

MODEL_METRICS_PATH = os.path.join(
    MODEL_DIR,
    "model_metrics.pkl"
)


def get_model_info():

    if not os.path.exists(MODEL_NAME_PATH):

        return {
            "error": "No trained model found"
        }

    model_name = joblib.load(MODEL_NAME_PATH)

    problem_type = joblib.load(PROBLEM_TYPE_PATH)

    metrics = {}

    if os.path.exists(MODEL_METRICS_PATH):
        metrics = joblib.load(MODEL_METRICS_PATH)

    response = {
        "model_name": model_name,
        "problem_type": problem_type,
        "training_status": "completed"
    }

    if problem_type == "classification":

        response["accuracy"] = metrics.get("accuracy")
        response["precision"] = metrics.get("precision")
        response["recall"] = metrics.get("recall")
        response["f1_score"] = metrics.get("f1_score")

    else:

        response["r2_score"] = metrics.get("R2")
        response["mae"] = metrics.get("MAE")
        response["rmse"] = metrics.get("RMSE")
        response["mse"] = metrics.get("MSE")

    return response