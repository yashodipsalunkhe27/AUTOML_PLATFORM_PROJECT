import os
import joblib
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Paths
# ----------------------------
MODEL_PATH = "models/production/best_model.pkl"
FEATURE_NAMES_PATH = "models/artifacts/feature_names.pkl"
FEATURE_IMPORTANCE_PATH = "models/artifacts/feature_importance.pkl"
GRAPH_PATH = "graphs/feature_importance.png"


def generate_feature_importance_graph(model=None, feature_names=None):

    # ----------------------------
    # Create folders
    # ----------------------------
    os.makedirs("graphs", exist_ok=True)
    os.makedirs("models/artifacts", exist_ok=True)

    # ----------------------------
    # Load trained model
    # ----------------------------
    if model is None:

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found: {MODEL_PATH}"
            )

        model = joblib.load(MODEL_PATH)

    # ----------------------------
    # Load feature names
    # ----------------------------
    if feature_names is None:

        if not os.path.exists(FEATURE_NAMES_PATH):
            raise FileNotFoundError(
                f"Feature names file not found: {FEATURE_NAMES_PATH}"
            )

        feature_names = joblib.load(FEATURE_NAMES_PATH)

    feature_names = list(feature_names)

    # ----------------------------
    # Get feature importance
    # (ONLY tree-based models allowed)
    # ----------------------------
    tree_based_only = (
        "DecisionTreeClassifier",
        "DecisionTreeRegressor",
        "RandomForestClassifier",
        "RandomForestRegressor",
        "ExtraTreesClassifier",
        "ExtraTreesRegressor",
        "XGBClassifier",
        "XGBRegressor",
        "CatBoostClassifier",
        "CatBoostRegressor",
    )

    if type(model).__name__ not in tree_based_only:
        raise ValueError(
            f"{type(model).__name__} does not support feature importance."
        )

    importances = model.feature_importances_

    # ----------------------------
    # Validation
    # ----------------------------
    if len(importances) != len(feature_names):

        raise ValueError(
            f"Mismatch: {len(importances)} importances but "
            f"{len(feature_names)} feature names."
        )

    # ----------------------------
    # Save importance list
    # ----------------------------
    feature_importance = []

    for feature, importance in zip(feature_names, importances):

        feature_importance.append(
            {
                "feature": feature,
                "importance": round(float(importance), 6)
            }
        )

    feature_importance.sort(
        key=lambda x: x["importance"],
        reverse=True
    )

    joblib.dump(
        feature_importance,
        FEATURE_IMPORTANCE_PATH
    )

    # ----------------------------
    # Plot graph
    # ----------------------------
    sorted_indices = np.argsort(importances)

    plt.figure(figsize=(10, 7))

    plt.barh(
        np.arange(len(sorted_indices)),
        importances[sorted_indices]
    )

    plt.yticks(
        np.arange(len(sorted_indices)),
        np.array(feature_names)[sorted_indices]
    )

    plt.xlabel("Importance")
    plt.ylabel("Features")
    plt.title("Feature Importance")

    plt.tight_layout()

    plt.savefig(GRAPH_PATH)

    plt.close()

    return GRAPH_PATH