
from importlib.resources import path
import traceback


from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import joblib
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd 
from src.batch_predict import batch_predict
from fastapi.responses import FileResponse
from datetime import datetime
from src.outlier_handler import remove_target_outliers
from src.feature_selector import select_features
from src.scaler import scale_features
from fastapi.responses import FileResponse, JSONResponse

from src.training_history import (
    save_training_history,
    get_training_history
)
# =========================
# INTERNAL MODULES
# =========================
from src.model_results import get_model_results
from src.model_comparison_graph import generate_model_comparison_graph
from src.confusion_matrix_graph import generate_confusion_matrix_graph
from src.classification_report_info import get_classification_report
from src.feature_importance_graph import generate_feature_importance_graph
from src.cross_validation import perform_cross_validation
from src.hyperparameter_tuning import tune_model
from src.load_data import load_dataset
import src.preprocessing as preprocessing
from src.split_data import split_dataset
from src.model_selector import get_model
from src.train_model import train_model as train_ml_model
from src.metrics import evaluate_model
from src.predict import predict_output
from src.dataset_analysis import analyze_dataset
from src.remove_id_columns import remove_id_columns
from src.remove_constant_columns import remove_constant_columns
from src.remove_duplicate_rows import remove_duplicate_rows
from src.handle_missing_values import handle_missing_values
from src.model_info import get_model_info
from src.correlation_heatmap import generate_correlation_heatmap
from src.roc_curve_graph import generate_roc_curve
from src.target_distribution_graph import (
    generate_target_distribution
)
from src.shap_summary_graph import generate_shap_summary
from src.dataset_statistics import get_dataset_statistics
from src.dataset_summary import get_dataset_summary
from src.prediction_schema import get_prediction_schema
from src.dataset_validator import validate_dataset
from src.report_generator import generate_training_report


from typing import Dict, Any
from urllib.parse import urljoin

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

# =========================
# URL HELPER
# =========================
def create_url(request: Request, endpoint: str):
    return urljoin(str(request.base_url), endpoint)

CURRENT_DATASET_PATH = None
CURRENT_DATASET_NAME = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
MODEL_DIR = os.path.join(BASE_DIR, "models")
GRAPH_DIR = os.path.join(BASE_DIR, "graphs")

PROD_DIR = os.path.join(MODEL_DIR, "production")
ARTIFACT_DIR = os.path.join(MODEL_DIR, "artifacts")
ENCODER_DIR = os.path.join(MODEL_DIR, "encoders")


# ✅ ADD THIS HERE
FEATURE_PATH = os.path.join(ARTIFACT_DIR, "feature_names.pkl")

import matplotlib
matplotlib.use("Agg")

# =========================
# APP INIT
# =========================
app = FastAPI(
    title="AutoML Platform",
    version="2.0.0",
    description="Automatic Machine Learning Platform"
)

# =========================
# CORS CONFIGURATION
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================
# DIRECTORIES
# =========================

directories = [
    UPLOAD_DIR,
    MODEL_DIR,
    GRAPH_DIR,
    PROD_DIR,
    ARTIFACT_DIR,
    ENCODER_DIR
]

for d in directories:
    os.makedirs(d, exist_ok=True)

app.mount("/graphs", StaticFiles(directory=GRAPH_DIR), name="graphs")

MODEL_PATH = os.path.join(PROD_DIR, "best_model.pkl")


# =========================
# HOME
# =========================
@app.get("/")
def home():
    return {"message": "ML Training API Running Successfully 🚀"}


# =========================
# UPLOAD DATASET
# =========================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    allowed_extensions = [
        ".csv",
        ".xlsx",
        ".json"
    ]

    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}"
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        "current_dataset" + ext
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    global CURRENT_DATASET_PATH, CURRENT_DATASET_NAME

    CURRENT_DATASET_PATH = file_path
    CURRENT_DATASET_NAME = file.filename
    

    try:
        df = load_dataset(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid dataset: {str(e)}"
        )

    return {
        "message": "Dataset uploaded successfully",
        "filename": file.filename,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1])
    }
# =========================
# DATASET ANALYSIS
# =========================
@app.get("/dataset-analysis")
def dataset_analysis_api():

    global CURRENT_DATASET_PATH

    if CURRENT_DATASET_PATH is None:
        raise HTTPException(
            status_code=400,
            detail="Upload dataset first"
        )

    df = load_dataset(CURRENT_DATASET_PATH)

    return analyze_dataset(df)
# =========================
# TRAIN MODEL
# =========================
@app.post("/train")
def train_model_api(target_column: str):

    global CURRENT_DATASET_PATH

    # =========================
    # CHECK DATASET UPLOADED
    # =========================
    if CURRENT_DATASET_PATH is None:
        raise HTTPException(
            status_code=400,
            detail="Upload dataset first"
        )

    # =========================
    # LOAD DATASET
    # =========================
    df = load_dataset(CURRENT_DATASET_PATH)

    # =========================
    # DATASET VALIDATION
    # =========================
    validate_dataset(
        df,
        target_column
    )

    # =========================
    # REMOVE ID COLUMNS
    # =========================
    df = remove_id_columns(df)
    # =========================
    # CLEANING
    # =========================
    
    df, removed_constant_columns = remove_constant_columns(df)

    df, removed_duplicate_rows = remove_duplicate_rows(df)

    df = handle_missing_values(df)

    # Remove target outliers for regression

    if (
        pd.api.types.is_numeric_dtype(
            df[target_column]
        )
        and
        df[target_column].nunique() > 20
    ):

        df = remove_target_outliers(
            df,
            target_column
        )

    # =========================
    # TARGET DISTRIBUTION GRAPH
    # =========================
    if target_column not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Target column '{target_column}' was removed during preprocessing."
        )

    generate_target_distribution(
        df,
        target_column
    )
    
    # =========================
    # SPLIT FEATURES / TARGET
    # =========================
    X = df.drop(columns=[target_column])

    y = df[target_column]


    # =========================
    # PROBLEM TYPE DETECTION
    # =========================
    from pandas.api.types import (
        is_numeric_dtype,
        is_string_dtype
    )

    if is_string_dtype(y):
        problem_type = "classification"

    elif is_numeric_dtype(y):

        if y.nunique() <= 10:
            problem_type = "classification"
        else:
            problem_type = "regression"

    else:
        problem_type = "classification"

    print(f"Detected Problem Type: {problem_type}")

    # =========================
    # REMOVE OLD ARTIFACTS & GRAPHS
    # =========================
    old_files = [

        # Feature Importance
        os.path.join(ARTIFACT_DIR, "feature_importance.pkl"),
        os.path.join(GRAPH_DIR, "feature_importance.png"),

        # SHAP
        os.path.join(GRAPH_DIR, "shap_summary.png"),

        # ROC
        os.path.join(GRAPH_DIR, "roc_curve.png"),
        os.path.join(ARTIFACT_DIR, "roc_y_test.pkl"),
        os.path.join(ARTIFACT_DIR, "roc_y_probs.pkl"),

        # Confusion Matrix
        os.path.join(GRAPH_DIR, "confusion_matrix.png"),
        os.path.join(ARTIFACT_DIR, "confusion_matrix.pkl"),

        # Reports
        os.path.join(ARTIFACT_DIR, "classification_report.pkl"),
        os.path.join(ARTIFACT_DIR, "regression_report.pkl")
    ]

    for file_path in old_files:
        if os.path.exists(file_path):
            os.remove(file_path)

    if len(df[target_column].unique()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Target column must contain at least 2 classes."
        )


    # =========================
    # PREPROCESSING
    # =========================
    df_clean = X.copy()
    df_clean[target_column] = y

    df_clean = preprocessing.preprocess_data(
        df_clean,
        target_column
    )

    print("\n===== CHECK TARGET =====")
    print(df_clean[target_column].dtype)
    print(df_clean[target_column].unique())

    if df_clean.empty:
        raise HTTPException(
            status_code=400,
            detail="Dataset became empty after preprocessing."
        )

    # =========================
    # Split Features & Target
    # =========================
    X_cv = df_clean.drop(columns=[target_column])
    y_cv = df_clean[target_column]

    # =========================
    # SAVE ORIGINAL FEATURE NAMES
    # =========================
    joblib.dump(
        X_cv.columns.tolist(),
        os.path.join(
            ARTIFACT_DIR,
            "original_feature_names.pkl"
        )
    )

    print("\n===== REQUIRED FEATURES =====")

    # =========================
    # Feature Selection
    # =========================
    X_cv = select_features(
        X_cv,
        y_cv,
        problem_type
    )

    # =========================
    # Feature Scaling
    # =========================
    X_cv = scale_features(X_cv)

    # Rebuild dataframe
    df_clean = X_cv.copy()
    df_clean[target_column] = y_cv

    print("\n===== TARGET AFTER PREPROCESSING =====")
    print(y_cv.value_counts())

    print("\n===== UNIQUE TARGET VALUES =====")
    print(y_cv.unique())
    # =========================
    # DATASET SIZE CHECK
    # =========================
    if X_cv.shape[0] < 20:
        raise HTTPException(
            status_code=400,
            detail="Dataset too small for training. Minimum 20 rows required."
        )


    if y_cv.isnull().sum() > 0:
        raise HTTPException(
            status_code=400,
            detail="Target column contains missing values."
        )
    # =========================
    # CLASS BALANCE CHECK
    # =========================
    if problem_type == "classification":

        class_counts = y_cv.value_counts()

        if class_counts.min() < 5:
            raise HTTPException(
                status_code=400,
                detail="Each target class must contain at least 5 samples."
            )

    # =========================
    # CROSS VALIDATION
    # =========================
    try:
        cv_results = perform_cross_validation(
            X_cv,
            y_cv,
            problem_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Cross validation failed: {str(e)}"
        )

    # =========================
    # SAVE FEATURE NAMES
    # =========================
    joblib.dump(
        X_cv.columns.tolist(),
        FEATURE_PATH
    )

    joblib.dump(
    problem_type,
    os.path.join(
        ARTIFACT_DIR,
        "problem_type.pkl"
    )
)

    # =========================
    # SAVE TARGET COLUMNS
    # =========================

    joblib.dump(
    target_column,
    os.path.join(
        ARTIFACT_DIR,
        "target_column.pkl"
    )
)
    
    # =========================
    # TRAIN TEST SPLIT
    # =========================
    try:
        X_train, X_test, y_train, y_test = split_dataset(
            df_clean,
            target_column
        )

        print("\n===== y_train INFO =====")
        print(type(y_train))
        print(y_train.shape)

        print("\n===== y_test INFO =====")
        print(type(y_test))
        print(y_test.shape)

        print("\n===== X_train INFO =====")
        print(type(X_train))
        print(X_train.shape)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Train-test split failed: {str(e)}"
        )

    if problem_type == "classification":

        if len(y_train.unique()) < 2:
            raise HTTPException(
                status_code=400,
                detail="Training set contains only one class."
            )
    # =========================
    # MODELS
    # =========================
    if problem_type == "classification":
        models = {
            "logistic": get_model("logistic"),
            "decision_tree": get_model("decision_tree"),
            "random_forest": get_model("random_forest"),
            "svm": get_model("svm"),
            "knn": get_model("knn"),
            "extra_trees_classifier":
                get_model("extra_trees_classifier"),
            "xgboost_classifier":
                get_model("xgboost_classifier"),
            "catboost_classifier":
                get_model("catboost_classifier")
        }

    else:
        models = {
            "linear_regression":
                get_model("linear_regression"),

            "decision_tree_regressor":
                get_model("decision_tree_regressor"),

            "random_forest_regressor":
                get_model("random_forest_regressor"),

            "svr":
                get_model("svr"),

            "knn_regressor":
                get_model("knn_regressor"),

            "extra_trees_regressor":
                get_model("extra_trees_regressor"),

            "xgboost_regressor":
                get_model("xgboost_regressor"),

            "catboost_regressor":
                get_model("catboost_regressor")
        }
    results = {}
    best_model = None
    best_name = ""
    best_acc = float("-inf")
    best_report = None

    for name, model in models.items():
        try:
            trained = train_ml_model(
                model,
                X_train,
                y_train
            )

            acc, _, report = evaluate_model(
                trained,
                X_test,
                y_test,
                problem_type
            )

            results[MODEL_NAMES.get(name, name)] = {
                "score": round(acc, 4)
            }


            if acc > best_acc:
                best_model = trained
                best_name = name
                best_acc = acc
                best_report = report

        except Exception as e:
            print(f"\n{name} failed")
            traceback.print_exc()

    # =========================
    # SAFETY CHECK
    # =========================
    if best_model is None:
        raise HTTPException(
            status_code=500,
            detail="No valid model could be trained."
        )

    # =========================
    # TUNING
    # =========================
    try:
        tuned_model, best_params, cv_score = tune_model(
            best_name,
            best_model,
            X_train,
            y_train,
            problem_type
        )

    except Exception as e:
        print("Tuning Error:", e)

        tuned_model = best_model
        best_params = {}
        cv_score = 0

    best_model = tuned_model

    best_acc, _, best_report = evaluate_model(
        best_model,
        X_test,
        y_test,
        problem_type
    )

    print("=" * 50)
    print(type(best_model))
    print(best_model)
    print("=" * 50)
    # =========================
    # PREDICTIONS
    # =========================

    try:
        preds = best_model.predict(X_test)
        print(type(preds))
        print(preds.shape)
        print(preds[:5])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction generation failed: {str(e)}"
        )

    print("\n===== TRAIN TARGET =====")
    print(y_train.value_counts())

    print("\n===== TEST TARGET =====")
    print(y_test.value_counts())

    print("\n===== PREDICTIONS =====")

    preds = np.asarray(preds).reshape(-1)

    print(pd.Series(preds).value_counts())
    
    if hasattr(best_model, "predict_proba"):

        probs = best_model.predict_proba(X_test)

        if probs.ndim == 2 and probs.shape[1] == 2:

            y_probs = probs[:, 1]

        else:

            y_probs = None

    elif hasattr(best_model, "decision_function"):

        scores = best_model.decision_function(X_test)

        if np.asarray(scores).ndim == 1:

            y_probs = scores

        else:

            y_probs = None

    else:

        y_probs = None
    # =========================
    # CLASSIFICATION ONLY
    # =========================
    if problem_type == "classification":

        # ROC Curve

        joblib.dump(
            y_test,
            os.path.join(
                ARTIFACT_DIR,
                "roc_y_test.pkl"
            )
        )

        joblib.dump(
            y_probs,
            os.path.join(
                ARTIFACT_DIR,
                "roc_y_probs.pkl"
            )
        )

        if (y_probs is not None and len(np.unique(y_test)) == 2):
            generate_roc_curve(
                y_test,
                y_probs
            )


        print("\nActual class distribution:")
        print(y_test.value_counts())

        print("\nPredicted class distribution:")
        print(pd.Series(preds).value_counts())

        # Confusion Matrix

        cm = confusion_matrix(
            y_test,
            preds
        )

        print("\n==============================")
        print("CONFUSION MATRIX")
        print("==============================")
        print(cm)

        joblib.dump(
            cm,
            os.path.join(
                ARTIFACT_DIR,
                "confusion_matrix.pkl"
            )
        )

        generate_confusion_matrix_graph(cm)

    # =========================
    # SAVE ENCODERS
    # =========================
    print("\n===== SAVING FEATURE ENCODERS =====")
    print(preprocessing.feature_encoders.keys())

    joblib.dump(
        preprocessing.feature_encoders,
        os.path.join(
            ENCODER_DIR,
            "feature_encoders.pkl"
        )
    )

    joblib.dump(
        preprocessing.target_encoder,
        os.path.join(
            ENCODER_DIR,
            "target_encoder.pkl"
        )
    )

    # =========================
    # SAVE MODEL
    # =========================
    joblib.dump(best_model, MODEL_PATH)

    joblib.dump(
        MODEL_NAMES.get(best_name, best_name),
        os.path.join(MODEL_DIR, "model_name.pkl")
    )

    joblib.dump(
        round(best_acc, 4),
        os.path.join(MODEL_DIR, "model_score.pkl")
    )

    joblib.dump(
        results,
        os.path.join(MODEL_DIR, "model_results.pkl")
    )

    joblib.dump(
        best_params,
        os.path.join(MODEL_DIR, "best_params.pkl")
    )

    # Save complete evaluation report
    joblib.dump(
        best_report,
        os.path.join(MODEL_DIR, "model_metrics.pkl")
    )


    if problem_type == "classification":

        joblib.dump(
            best_report,
            os.path.join(
                ARTIFACT_DIR,
                "classification_report.pkl"
            )
        )

    else:

        joblib.dump(
            best_report,
            os.path.join(
                ARTIFACT_DIR,
                "regression_report.pkl"
            )
        )

    history_record = {

        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "dataset": CURRENT_DATASET_NAME,

        "problem_type": problem_type,

        "best_model": MODEL_NAMES.get(best_name, best_name),

        "best_parameters": best_params

    }

    if problem_type == "classification":

        history_record["accuracy"] = round(best_acc, 4)

    else:

        history_record["r2_score"] = round(best_acc, 4)

    save_training_history(history_record)

    # =========================
    # GENERATE PDF REPORT
    # =========================
    generate_training_report(

        dataset_name=CURRENT_DATASET_NAME,

        rows=len(df),

        columns=len(df.columns)

    )
       # =========================
       # GRAPHS
       # =========================

        # Model Comparison
    generate_model_comparison_graph()

        # ---------------------------------
        # Feature Importance
        # ---------------------------------

    feature_importance_supported = (
            "DecisionTreeClassifier",
            "DecisionTreeRegressor",
            "RandomForestClassifier",
            "RandomForestRegressor",
            "ExtraTreesClassifier",
            "ExtraTreesRegressor",
            "XGBClassifier",
            "XGBRegressor",
            "CatBoostClassifier",
            "CatBoostRegressor"
        )

    if type(best_model).__name__ in feature_importance_supported:

            try:

                generate_feature_importance_graph(
                    best_model,
                    X_cv.columns
                )

            except Exception as e:

                print("Feature Importance Error:", e)

    else:

        print(
            "Feature Importance not supported."
        )

        fi = os.path.join(
            ARTIFACT_DIR,
            "feature_importance.pkl"
        )

        fig = os.path.join(
            GRAPH_DIR,
            "feature_importance.png"
        )

        if os.path.exists(fi):
            os.remove(fi)

        if os.path.exists(fig):
            os.remove(fig)

    # ---------------------------------
    # SHAP Summary
    # ---------------------------------

    shap_supported = (
        "DecisionTreeClassifier",
        "DecisionTreeRegressor",
        "RandomForestClassifier",
        "RandomForestRegressor",
        "ExtraTreesClassifier",
        "ExtraTreesRegressor",
        "XGBClassifier",
        "XGBRegressor"
        )

    if type(best_model).__name__ in shap_supported:

            try:
                sample_data = X_train.sample(
                    min(100, len(X_train)),
                    random_state=42
                )

                generate_shap_summary(
                    best_model,
                    sample_data
                )

            except Exception:

                print("\nSHAP Summary not supported for this model.")

                shap_file = "graphs/shap_summary.png"

                if os.path.exists(shap_file):
                    os.remove(shap_file)
        # =========================
        # RESPONSE
        # =========================

    response = {

            "problem_type": problem_type,

            "all_model_results": results,

            "best_model": MODEL_NAMES.get(best_name, best_name),

            "best_parameters": best_params,

            "tuning_cv_score": round(cv_score, 4),

            "cross_validation": cv_results,

            "removed_constant_columns": removed_constant_columns,

            "removed_duplicate_rows": removed_duplicate_rows,

            "message": "Training completed successfully"

        }

    if problem_type == "classification":

            response["best_accuracy"] = round(best_acc, 4)

    else:

        response["best_score"] = round(best_acc, 4)

    return response

@app.get("/dataset-statistics")
def dataset_statistics_api():

    if CURRENT_DATASET_PATH is None:
        raise HTTPException(
            status_code=400,
            detail="Upload dataset first"
        )

    df = load_dataset(CURRENT_DATASET_PATH)

    return get_dataset_statistics(df)

# =========================
# DATASET SUMMARY
# =========================
@app.get("/dataset-summary")
def dataset_summary_api():

    if CURRENT_DATASET_PATH is None:
        raise HTTPException(
            status_code=400,
            detail="Upload dataset first."
        )

    df = load_dataset(CURRENT_DATASET_PATH)

    return get_dataset_summary(df)

# =========================
# MODEL INFO
# =========================
@app.get("/model-info")
def model_info():
    return get_model_info()


@app.get("/model-results")
def model_results():

    if not os.path.exists(MODEL_PATH):
        raise HTTPException(
            status_code=404,
            detail="Train model first."
        )

    return get_model_results()

#========================================
#   Classification Report EndPoint
#========================================
@app.get("/classification-report")
def classification_report():

    problem_path = os.path.join(
        ARTIFACT_DIR,
        "problem_type.pkl"
    )

    report_path = os.path.join(
        ARTIFACT_DIR,
        "classification_report.pkl"
    )

    if not os.path.exists(problem_path):
        return {
            "message": "No trained model available."
        }

    if not os.path.exists(report_path):
        return {
            "message": "Classification report not available."
        }

    problem_type = joblib.load(problem_path)

    if problem_type != "classification":
        return {
            "message":"Classification report is available only for classification models."
        }

    return joblib.load(report_path)
#========================================
#   Regression Report EndPoint
#========================================

@app.get("/regression-report")
def regression_report():

    problem_path = os.path.join(
        ARTIFACT_DIR,
        "problem_type.pkl"
    )

    report_path = os.path.join(
        ARTIFACT_DIR,
        "regression_report.pkl"
    )

    if not os.path.exists(problem_path):
        return {
            "message":"No trained model available."
        }

    if not os.path.exists(report_path):
        return {
            "message":"Regression report not available."
        }

    problem_type = joblib.load(problem_path)

    if problem_type != "regression":
        return {
            "message":"Regression report is available only for regression models."
        }

    return joblib.load(report_path)
# =========================
# GRAPH ENDPOINTS
# =========================
@app.get("/correlation-heatmap")
def correlation_heatmap_api(request: Request):

    global CURRENT_DATASET_PATH

    if CURRENT_DATASET_PATH is None:
        raise HTTPException(
            status_code=404,
            detail="Upload dataset first"
        )

    try:
        df = load_dataset(CURRENT_DATASET_PATH)

        generate_correlation_heatmap(df)

        graph_path = os.path.join(
            GRAPH_DIR,
            "correlation_heatmap.png"
        )

        if not os.path.exists(graph_path):
            raise HTTPException(
                status_code=404,
                detail="Heatmap not found."
            )

        return {
            "graph_url": create_url(
                request,
                "graphs/correlation_heatmap.png"
            )
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Heatmap generation failed: {str(e)}"
        )
@app.get("/model-comparison-graph")
def model_comparison_graph(request: Request):

    graph_path = os.path.join(
        GRAPH_DIR,
        "model_comparison.png"
    )

    if not os.path.exists(graph_path):
        raise HTTPException(
            status_code=404,
            detail="Graph not found."
        )

    return {
        "graph_url":
        str(request.base_url)
        + "graphs/model_comparison.png"
    }

@app.get("/feature-importance-graph")
def feature_importance_graph_api(request: Request):

    # Check model exists
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(
            status_code=404,
            detail="Train a model first."
        )

    model = joblib.load(MODEL_PATH)

    supported_models = (
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

    if type(model).__name__ not in supported_models:
        return {
            "message": "Feature importance graph is not supported for the selected model."
        }

    graph_path = os.path.join(GRAPH_DIR, "feature_importance.png")

    if not os.path.exists(graph_path):
        return {
            "message": "Feature importance graph is not available."
        }

    return {
        "graph_url": f"{request.base_url}graphs/feature_importance.png"
    }
    # =========================
    # LOAD CURRENT MODEL
    # =========================
    @app.get("/feature-importance")
    def feature_importance():

        if not os.path.exists(MODEL_PATH):
            return {
                "message":"No trained model available."
            }

        path = os.path.join(
            ARTIFACT_DIR,
            "feature_importance.pkl"
        )

        model = joblib.load(MODEL_PATH)

    # =========================
    # MODELS THAT SUPPORT FEATURE IMPORTANCE
    # =========================
    supported_models = (
        "DecisionTreeClassifier",
        "DecisionTreeRegressor",
        "RandomForestClassifier",
        "RandomForestRegressor",
        "ExtraTreesClassifier",
        "ExtraTreesRegressor",
        "XGBClassifier",
        "XGBRegressor",
        "CatBoostClassifier",
        "CatBoostRegressor"
    )

    # =========================
    # CHECK SUPPORT
    # =========================
    if type(model).__name__ not in supported_models:
        return {
            "message": "Feature importance graph is not supported for the selected model."
        }

    # =========================
    # CHECK GRAPH EXISTS
    # =========================
    graph_path = os.path.join(
        GRAPH_DIR,
        "feature_importance.png"
    )

    if not os.path.exists(graph_path):
        return {
            "message": "Feature importance graph is not available."
        }

    # =========================
    # RETURN GRAPH URL
    # =========================
    return {
        "graph_url": str(request.base_url) + "graphs/feature_importance.png"
    }

@app.get("/feature-importance")
def feature_importance():

    path = os.path.join(
        ARTIFACT_DIR,
        "feature_importance.pkl"
    )

    model = joblib.load(MODEL_PATH)

    supported = (

        "DecisionTreeClassifier",
        "DecisionTreeRegressor",
        "RandomForestClassifier",
        "RandomForestRegressor",
        "ExtraTreesClassifier",
        "ExtraTreesRegressor",
        "XGBClassifier",
        "XGBRegressor",
        "CatBoostClassifier",
        "CatBoostRegressor"

    )

    if type(model).__name__ not in supported:

        return {
            "message":"Feature importance is not supported for the selected model."
        }

    if not os.path.exists(path):

        return {
            "message":"Feature importance is not available."
        }

    return {
        "feature_importance":joblib.load(path)
    }


@app.get("/confusion-matrix-graph")
def confusion_matrix_graph(request: Request):

    problem_path = os.path.join(
        ARTIFACT_DIR,
        "problem_type.pkl"
    )

    if not os.path.exists(problem_path):
        return {
            "message":"No trained model available."
        }

    problem_type = joblib.load(problem_path)

    if problem_type != "classification":
        return {
            "message":"Confusion Matrix is available only for classification models."
        }

    graph_path = os.path.join(
        GRAPH_DIR,
        "confusion_matrix.png"
    )

    if not os.path.exists(graph_path):
        return {
            "message":"Confusion matrix graph not available."
        }

    return {
        "graph_url": str(request.base_url) + "graphs/confusion_matrix.png"
    }


@app.get("/roc-curve-graph")
def roc_curve_graph(request: Request):

    problem_path = os.path.join(
        ARTIFACT_DIR,
        "problem_type.pkl"
    )

    if not os.path.exists(problem_path):
        return {
            "message":"No trained model available."
        }

    problem_type = joblib.load(problem_path)

    if problem_type != "classification":
        return {
            "message":"ROC Curve is available only for classification models."
        }

    graph_path = os.path.join(
        GRAPH_DIR,
        "roc_curve.png"
    )

    if not os.path.exists(graph_path):
        return {
            "message":"ROC curve graph not available."
        }

    return {
        "graph_url": str(request.base_url) + "graphs/roc_curve.png"
    }

@app.get("/shap-summary")
def shap_summary_api():

    graph_path = "graphs/shap_summary.png"

    if os.path.exists(graph_path):

        return FileResponse(
            graph_path,
            media_type="image/png"
        )

    return JSONResponse(
        status_code=200,
        content={
            "message": "SHAP summary is not supported for the selected model."
        }
    )
@app.get("/model-status")
def model_status():

    model_exists = os.path.exists(MODEL_PATH)

    problem_type = None
    best_model = None
    score = None

    if model_exists:

        problem_path = os.path.join(
            ARTIFACT_DIR,
            "problem_type.pkl"
        )

        if os.path.exists(problem_path):
            problem_type = joblib.load(problem_path)

        model_name_path = os.path.join(
            MODEL_DIR,
            "model_name.pkl"
        )

        score_path = os.path.join(
            MODEL_DIR,
            "model_score.pkl"
        )

        if os.path.exists(model_name_path):
            best_model = joblib.load(model_name_path)

        if os.path.exists(score_path):
            score = joblib.load(score_path)

    return {
        "model_exists": model_exists,
        "status": "trained" if model_exists else "not_trained",
        "problem_type": problem_type,
        "best_model": MODEL_NAMES.get(best_model, best_model),
        "score": score
    }

@app.get("/model-performance")
def model_performance():

    if not os.path.exists(MODEL_PATH):
        raise HTTPException(
            status_code=404,
            detail="Model not trained yet."
        )

    required_files = [
        os.path.join(ARTIFACT_DIR, "problem_type.pkl"),
        os.path.join(MODEL_DIR, "model_name.pkl"),
        os.path.join(MODEL_DIR, "model_score.pkl"),
        os.path.join(MODEL_DIR, "model_results.pkl"),
        os.path.join(MODEL_DIR, "best_params.pkl")
    ]

    for file_path in required_files:

        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=f"Missing required file: {os.path.basename(file_path)}"
            )

    return {
        "problem_type": joblib.load(
            os.path.join(
                ARTIFACT_DIR,
                "problem_type.pkl"
            )
        ),

        "best_model": MODEL_NAMES.get(
            joblib.load(
                os.path.join(
                    MODEL_DIR,
                    "model_name.pkl"
                )
            ),
            joblib.load(
                os.path.join(
                    MODEL_DIR,
                    "model_name.pkl"
                )
            )
        ),

        "score": joblib.load(
            os.path.join(
                MODEL_DIR,
                "model_score.pkl"
            )
        ),

        "best_parameters": joblib.load(
            os.path.join(
                MODEL_DIR,
                "best_params.pkl"
            )
        ),

        "all_models": joblib.load(
            os.path.join(
                MODEL_DIR,
                "model_results.pkl"
            )
        )
    }


@app.get("/training-history")
def training_history(
    page: int = 1,
    limit: int = 20
):

    return get_training_history(
        limit=limit,
        page=page
    )


@app.get("/dashboard")
def dashboard():

    dataset = {
        "rows": 0,
        "columns": 0
    }

    if CURRENT_DATASET_PATH and os.path.exists(CURRENT_DATASET_PATH):
        df = load_dataset(CURRENT_DATASET_PATH)

        dataset = {
            "rows": len(df),
            "columns": len(df.columns)
        }

    model_name = None
    score = None
    problem_type = None

    model_name_path = os.path.join(MODEL_DIR, "model_name.pkl")
    model_score_path = os.path.join(MODEL_DIR, "model_score.pkl")
    problem_path = os.path.join(ARTIFACT_DIR, "problem_type.pkl")

    if os.path.exists(model_name_path):
        model_name = joblib.load(model_name_path)

    if os.path.exists(model_score_path):
        score = joblib.load(model_score_path)

    if os.path.exists(problem_path):
        problem_type = joblib.load(problem_path)

    return {
        "dataset": dataset,

        "model": {
            "name": model_name,
            "score": score,
            "problem_type": problem_type
        },

        "graphs": {

            "roc": os.path.exists(
                os.path.join(GRAPH_DIR, "roc_curve.png")
            ),

            "confusion": os.path.exists(
                os.path.join(GRAPH_DIR, "confusion_matrix.png")
            ),

            "feature_importance": os.path.exists(
                os.path.join(GRAPH_DIR, "feature_importance.png")
            ),

            "shap": os.path.exists(
                os.path.join(GRAPH_DIR, "shap_summary.png")
            )
        }
    }
# =========================
# MODEL METADATA
# =========================
@app.get("/model-metadata")
def model_metadata():

    if not os.path.exists(FEATURE_PATH):
        raise HTTPException(
            status_code=404,
            detail="Train model first."
        )

    problem_type = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "problem_type.pkl"
        )
    )

    feature_names = joblib.load(
        FEATURE_PATH
    )

    return {
        "problem_type": problem_type,
        "required_features": feature_names
    }

# =========================
# PREDICTION SCHEMA
# =========================
@app.get("/prediction-schema")
def prediction_schema():

    return get_prediction_schema()


# =========================
# PREDICT
# =========================
@app.post("/predict")
def predict_api(data: Dict[str, Any]):
    try:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(
                status_code=404,
                detail="Model not trained yet"
            )

        # =========================
        # Load required features
        # =========================
        
        if not os.path.exists(FEATURE_PATH):
            raise HTTPException(
                status_code=404,
                detail="Feature file not found. Train model first."
            )
        
        input_data = data

        # Let predict.py handle preprocessing
        return predict_output(input_data)
    
    except HTTPException:
        raise

    except Exception as e:
        print("PREDICT ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Prediction Error: {str(e)}"
        )
    
# =========================
# BATCH PREDICTION
# =========================
@app.post("/batch-predict")
async def batch_predict_api(
    request: Request,
    file: UploadFile = File(...)
):

    # =========================
    # CHECK MODEL TRAINED
    # =========================
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(
            status_code=404,
            detail="Train model first."
        )

    # =========================
    # CHECK PROBLEM TYPE EXISTS
    # =========================
    problem_type_path = os.path.join(
        ARTIFACT_DIR,
        "problem_type.pkl"
    )

    if not os.path.exists(problem_type_path):
        raise HTTPException(
            status_code=404,
            detail="Problem type not found. Train model first."
        )

    # =========================
    # LOAD PROBLEM TYPE
    # =========================
    problem_type = joblib.load(
        problem_type_path
    )

    # =========================
    # VALIDATE FILE TYPE
    # =========================
    allowed_extensions = [
        ".csv",
        ".xlsx",
        ".json"
    ]

    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=404,
            detail=f"Unsupported file type: {ext}"
        )
    
    # =========================
    # SAVE UPLOADED FILE
    # =========================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    temp_path = os.path.join(
        UPLOAD_DIR,
        f"{timestamp}_{file.filename}"
    )

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # =========================
    # RUN BATCH PREDICTION
    # =========================
    try:
        result_df = batch_predict(temp_path)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )

    # =========================
    # SAVE OUTPUT CSV
    # =========================
    output_path = os.path.join(
        UPLOAD_DIR,
        "predictions.csv"
    )

    result_df.to_csv(
        output_path,
        index=False
    )

    if os.path.exists(temp_path):
        os.remove(temp_path)

    response = {
        "status": "success",
        "message": "Batch prediction completed successfully",
        "problem_type": problem_type,
        "rows_processed": len(result_df),
        "download_url": str(request.base_url) + "download-predictions"
    }

    # =========================
    # CLASSIFICATION SUMMARY
    # =========================
    if (
        problem_type == "classification"
        and "Prediction" in result_df.columns
    ):

        response["prediction_summary"] = (
            result_df["Prediction"]
            .value_counts()
            .to_dict()
        )

    # =========================
    # REGRESSION SUMMARY
    # =========================
    elif (
        problem_type == "regression"
        and "Prediction" in result_df.columns
    ):

        response["regression_summary"] = {
            "average": round(float(result_df["Prediction"].mean()), 2),
            "minimum": round(float(result_df["Prediction"].min()), 2),
            "maximum": round(float(result_df["Prediction"].max()), 2),
        }

    return response
# =========================
# DOWNLOAD PREDICTIONS
# =========================
@app.get("/download-predictions")
def download_predictions():

    file_path = os.path.join(
        UPLOAD_DIR,
        "predictions.csv"
    )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Prediction file not found"
        )

    return FileResponse(
        path=file_path,
        filename="predictions.csv",
        media_type="text/csv"
    )

# =========================
# DOWNLOAD MODEL
# =========================
@app.get("/download-model")
def download_model():

    if not os.path.exists(MODEL_PATH):
        raise HTTPException(
            status_code=404,
            detail="Model not found"
        )

    return FileResponse(
        path=MODEL_PATH,
        filename="best_model.pkl",
        media_type="application/octet-stream"
    )

# =========================
# DOWNLOAD FEATURES
# =========================

@app.get("/download-features")
def download_features():

    if not os.path.exists(FEATURE_PATH):
        raise HTTPException(
            status_code=404,
            detail="Feature file not found"
        )

    return FileResponse(
        path=FEATURE_PATH,
        filename="feature_names.pkl",
        media_type="application/octet-stream"
    )

# =========================
# DOWNLOAD TRAINING REPORT
# =========================
@app.get("/download-training-report")
def download_training_report():

    report_path = "reports/Training_Report.pdf"

    if not os.path.exists(report_path):

        raise HTTPException(

            status_code=404,

            detail="Training report not found."

        )

    return FileResponse(

        path=report_path,

        filename="Training_Report.pdf",

        media_type="application/pdf"

    )

# =========================
# DELETE MODEL
# =========================
@app.delete("/delete-model")
def delete_model():

    files_to_delete = [

        # Models
        MODEL_PATH,
        os.path.join(MODEL_DIR, "model_name.pkl"),
        os.path.join(MODEL_DIR, "model_score.pkl"),
        os.path.join(MODEL_DIR, "model_results.pkl"),
        os.path.join(MODEL_DIR, "best_params.pkl"),

        # Artifacts
        os.path.join(ARTIFACT_DIR, "classification_report.pkl"),
        os.path.join(ARTIFACT_DIR,"regression_report.pkl"),
        os.path.join(ARTIFACT_DIR, "feature_names.pkl"),
        os.path.join(ARTIFACT_DIR, "problem_type.pkl"),
        os.path.join(ARTIFACT_DIR, "target_column.pkl"),
        os.path.join(ARTIFACT_DIR, "confusion_matrix.pkl"),
        os.path.join(ARTIFACT_DIR,"selector.pkl"),
        os.path.join(ARTIFACT_DIR, "scaler.pkl"),
        os.path.join(ARTIFACT_DIR, "roc_y_test.pkl"),
        os.path.join(ARTIFACT_DIR, "roc_y_probs.pkl"),
        os.path.join(ARTIFACT_DIR,"feature_importance.pkl"),
        os.path.join(ARTIFACT_DIR,"original_feature_names.pkl"),
        os.path.join(ARTIFACT_DIR,"roc_data.pkl"),

        # Encoders
        os.path.join(ENCODER_DIR, "feature_encoders.pkl"),
        os.path.join(ENCODER_DIR, "target_encoder.pkl"),

        # Graphs
        os.path.join(GRAPH_DIR, "confusion_matrix.png"),
        os.path.join(GRAPH_DIR, "roc_curve.png"),
        os.path.join(GRAPH_DIR, "feature_importance.png"),
        os.path.join(GRAPH_DIR, "shap_summary.png"),
        os.path.join(GRAPH_DIR, "model_comparison.png"),
        os.path.join(GRAPH_DIR, "correlation_heatmap.png"),
        os.path.join(GRAPH_DIR, "target_distribution.png")
    ]

    deleted_files = []

    for file_path in files_to_delete:

        if os.path.exists(file_path):

            try:
                os.remove(file_path)

                deleted_files.append(
                    os.path.basename(file_path)
                )

            except Exception:
                continue

    return {
        "message": "Model deleted successfully",
        "deleted_count": len(deleted_files),
        "deleted_files": deleted_files
    }

