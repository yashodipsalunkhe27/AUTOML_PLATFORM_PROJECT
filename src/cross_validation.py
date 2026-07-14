from sklearn.model_selection import cross_val_score
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor
)


def perform_cross_validation(
    X,
    y,
    problem_type="classification"
):

    # =========================
    # CLASSIFICATION
    # =========================
    if problem_type == "classification":

        model = RandomForestClassifier(
            random_state=42
        )

        scores = cross_val_score(
            model,
            X,
            y,
            cv=5,
            scoring="accuracy"
        )

        return {
            "cv_scores": scores.tolist(),
            "mean_accuracy": round(scores.mean(), 4),
            "std_accuracy": round(scores.std(), 4)
        }

    # =========================
    # REGRESSION
    # =========================
    else:

        model = RandomForestRegressor(
            random_state=42
        )

        scores = cross_val_score(
            model,
            X,
            y,
            cv=5,
            scoring="r2"
        )

        return {
            "cv_scores": scores.tolist(),
            "mean_r2": round(scores.mean(), 4),
            "std_r2": round(scores.std(), 4)
        }