from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

from xgboost import XGBClassifier
from xgboost import XGBRegressor

from catboost import CatBoostClassifier
from catboost import CatBoostRegressor


def get_model(model_name):

    models = {

        # =========================
        # Classification
        # =========================
        "logistic": LogisticRegression(max_iter=1000,class_weight="balanced",random_state=42),
        "decision_tree": DecisionTreeClassifier(),
        "random_forest": RandomForestClassifier(),
        "svm": SVC(probability=True),
        "knn": KNeighborsClassifier(),
        "extra_trees_classifier": ExtraTreesClassifier(random_state=42),
        "xgboost_classifier": XGBClassifier(random_state=42,eval_metric="logloss"),
        "catboost_classifier": CatBoostClassifier(
            verbose=0,
            random_state=42
        ),

        # =========================
        # Regression
        # =========================
        "linear_regression": LinearRegression(),
        "decision_tree_regressor": DecisionTreeRegressor(),
        "random_forest_regressor": RandomForestRegressor(),
        "svr": SVR(),
        "knn_regressor": KNeighborsRegressor(),
        "extra_trees_regressor": ExtraTreesRegressor(random_state=42),
        "xgboost_regressor": XGBRegressor(random_state=42),
        "catboost_regressor": CatBoostRegressor(
            verbose=0,
            random_state=42
        )
    }

    return models[model_name]