from sklearn.model_selection import GridSearchCV


def tune_model(
    model_name,
    model,
    X_train,
    y_train,
    problem_type="classification"
):

    param_grid = {}

    # =========================
    # CLASSIFICATION MODELS
    # =========================

    if model_name == "logistic":

        param_grid = {
            "C": [0.01, 0.1, 1, 10, 100],
            "solver": ["liblinear", "lbfgs"]
        }

    elif model_name == "decision_tree":

        param_grid = {
            "max_depth": [3, 5, 10, None],
            "min_samples_split": [2, 5, 10]
        }

    elif model_name == "random_forest":

        param_grid = {
            "n_estimators": [50, 100, 200],
            "max_depth": [3, 5, 10, None],
            "min_samples_split": [2, 5]
        }

    elif model_name == "svm":

        param_grid = {
            "C": [0.1, 1, 10],
            "kernel": ["linear", "rbf"]
        }

    elif model_name == "knn":

        param_grid = {
            "n_neighbors": [3, 5, 7, 9]
        }

    # =========================
    # REGRESSION MODELS
    # =========================

    elif model_name == "linear_regression":

        param_grid = {}

    elif model_name == "decision_tree_regressor":

        param_grid = {
            "max_depth": [3, 5, 10, None],
            "min_samples_split": [2, 5, 10]
        }

    elif model_name == "random_forest_regressor":

        param_grid = {
            "n_estimators": [50, 100, 200],
            "max_depth": [3, 5, 10, None]
        }

    elif model_name == "svr":

        param_grid = {
            "C": [0.1, 1, 10],
            "kernel": ["linear", "rbf"]
        }

    elif model_name == "knn_regressor":

        param_grid = {
            "n_neighbors": [3, 5, 7, 9]
        }

    # =========================
    # SCORING
    # =========================

    scoring_metric = (
        "accuracy"
        if problem_type == "classification"
        else "r2"
    )

    # =========================
    # GRID SEARCH
    # =========================

    if param_grid:

        grid_search = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=5,
            scoring=scoring_metric,
            n_jobs=-1
        )

        grid_search.fit(
            X_train,
            y_train
        )

        return (
            grid_search.best_estimator_,
            grid_search.best_params_,
            grid_search.best_score_
        )

    return model, {}, 0