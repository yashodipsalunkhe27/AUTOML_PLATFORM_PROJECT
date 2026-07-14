import joblib
import os

MODEL_RESULTS_PATH = "models/model_results.pkl"

MODEL_NAMES = {

    "logistic": "Logistic Regression",

    "decision_tree": "Decision Tree",

    "random_forest": "Random Forest",

    "svm": "Support Vector Machine",

    "knn": "K-Nearest Neighbors",

    "extra_trees_classifier": "Extra Trees Classifier",

    "xgboost_classifier": "XGBoost Classifier",

    "catboost_classifier": "CatBoost Classifier",

    "linear_regression": "Linear Regression",

    "decision_tree_regressor": "Decision Tree Regressor",

    "random_forest_regressor": "Random Forest Regressor",

    "svr": "Support Vector Regressor",

    "knn_regressor": "K-Nearest Neighbors Regressor",

    "extra_trees_regressor": "Extra Trees Regressor",

    "xgboost_regressor": "XGBoost Regressor",

    "catboost_regressor": "CatBoost Regressor"
}


def get_model_results():

    if not os.path.exists(MODEL_RESULTS_PATH):

        return {
            "error": "No model results found"
        }

    results = joblib.load(MODEL_RESULTS_PATH)

    leaderboard = []

    for model_key, info in results.items():

        leaderboard.append({

            "model": MODEL_NAMES.get(model_key, model_key),

            "score": info["score"]

        })

    leaderboard.sort(

        key=lambda x: x["score"],

        reverse=True
    )

    for rank, row in enumerate(leaderboard, start=1):

        row["rank"] = rank

    return leaderboard