import os
import joblib
import pandas as pd

from sklearn.feature_selection import (
    SelectKBest,
    mutual_info_regression,
    mutual_info_classif
)

ARTIFACT_DIR = "models/artifacts"


def select_features(
    X,
    y,
    problem_type
):

    if problem_type == "regression":

        selector = SelectKBest(
            score_func=mutual_info_regression,
            k=min(20, X.shape[1])
        )

    else:

        selector = SelectKBest(
            score_func=mutual_info_classif,
            k=min(20, X.shape[1])
        )

    X_selected = selector.fit_transform(X, y)

    joblib.dump(
        selector,
        os.path.join(
            ARTIFACT_DIR,
            "selector.pkl"
        )
    )

    selected_columns = X.columns[
        selector.get_support()
    ]

    return pd.DataFrame(
        X_selected,
        columns=selected_columns,
        index=X.index
    )