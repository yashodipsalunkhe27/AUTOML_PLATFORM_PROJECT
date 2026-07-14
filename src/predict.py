import os
import joblib
import pandas as pd
from datetime import datetime

from src.model_loader import load_model

ENCODER_DIR = "models/encoders"
ARTIFACT_DIR = "models/artifacts"
MODEL_DIR = "models"


def predict_output(data):

    # =========================
    # Load Model
    # =========================
    model = load_model()

    # =========================
    # Load Problem Type
    # =========================
    problem_type = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "problem_type.pkl"
        )
    )

    # =========================
    # Load Feature Encoders
    # =========================
    feature_encoders = joblib.load(
        os.path.join(
            ENCODER_DIR,
            "feature_encoders.pkl"
        )
    )

    # Original feature names
    selected_feature_names = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "feature_names.pkl"
        )
    )

    target_encoder = joblib.load(
        os.path.join(
            ENCODER_DIR,
            "target_encoder.pkl"
        )
    )

    original_feature_names = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "original_feature_names.pkl"
        )
    )

    # =========================
    # Load Target Column
    # =========================
    target_column = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "target_column.pkl"
        )
    )

    # Feature Selector
    selector = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "selector.pkl"
        )
    )

    # Scaler
    scaler = joblib.load(
        os.path.join(
            ENCODER_DIR,
            "scaler.pkl"
        )
    )

    # =========================
    # Create DataFrame
    # =========================
    df = pd.DataFrame([data])

    print("\n===== INPUT =====")
    print(df)

    # =========================
    # Date Processing
    # =========================
    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day

        df.drop(
            columns=["date"],
            inplace=True
        )

    # =========================
    # Remove Street
    # =========================
    if "street" in df.columns:

        df.drop(
            columns=["street"],
            inplace=True
        )

    # =========================
    # Encode Categorical Columns
    # =========================
    for col, encoder in feature_encoders.items():

        if col in df.columns:

            df[col] = df[col].astype(str)

            df[[col]] = encoder.transform(
                df[[col]]
            )

    # =========================
    # Add Missing Original Features
    # =========================
    for col in original_feature_names:

        if col not in df.columns:
            df[col] = 0

    # =========================
    # Keep Original Training Order
    # =========================
    df = df[original_feature_names]

    # =========================
    # Feature Selection
    # =========================
    df = pd.DataFrame(
        selector.transform(df),
        columns=selected_feature_names
    )
    # =========================
    # Scaling
    # =========================
    df = pd.DataFrame(
        scaler.transform(df),
        columns=selected_feature_names
    )

    print("\n===== FINAL INPUT =====")
    print(df)

    # =========================
    # Prediction
    # =========================
    prediction = model.predict(df)[0]

    print(type(prediction))
    print(prediction)

    # Load professional model name
    model_name = joblib.load(
        os.path.join(
            MODEL_DIR,
            "model_name.pkl"
        )
    )

    if problem_type == "classification" and target_encoder is not None:
        prediction = target_encoder.inverse_transform([prediction])[0]

    # Convert numpy array -> scalar
    import numpy as np

    if isinstance(prediction, np.ndarray):
        prediction = prediction.item()

    # Convert float -> int if whole number
    if isinstance(prediction, (float, np.floating)):
        if prediction.is_integer():
            prediction = int(prediction)

    # =========================
    # Classification
    # =========================
    if problem_type == "classification":

        confidence = None

        if hasattr(model, "predict_proba"):

            probs = model.predict_proba(df)[0]

            confidence = float(max(probs))

        return {

            "problem_type": "classification",

            "target": target_column,

            "prediction": prediction,

            "confidence_percent": round(confidence * 100, 2),

            "model_used": model_name
        }
    
    print(type(prediction))
    print(prediction)
    # =========================
    # Regression
    # =========================
    return {

        "problem_type": "regression",

        "target": target_column,

        "predicted_value": int(round(prediction)),

        "unit": "USD",

        "model_used": model_name,

        "timestamp": datetime.now().strftime("%H:%M:%S")
    }