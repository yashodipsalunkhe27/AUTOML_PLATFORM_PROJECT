import os
import joblib
import pandas as pd
import numpy as np

from src.model_loader import load_model

ENCODER_DIR = "models/encoders"
ARTIFACT_DIR = "models/artifacts"


def batch_predict(file_path):

    # =========================
    # Load Model
    # =========================
    model = load_model()

    # =========================
    # Read File
    # =========================
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    else:
        raise Exception(
            "Only CSV and Excel files are supported."
        )

    # =========================
    # Load Artifacts
    # =========================
    feature_names = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "feature_names.pkl"
        )
    )

    original_feature_names = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "original_feature_names.pkl"
        )
    )

    selector = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "selector.pkl"
        )
    )

    scaler = joblib.load(
        os.path.join(
            ENCODER_DIR,
            "scaler.pkl"
        )
    )

    feature_encoders = joblib.load(
        os.path.join(
            ENCODER_DIR,
            "feature_encoders.pkl"
        )
    )

    problem_type = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "problem_type.pkl"
        )
    )

    # =========================
    # Debug
    # =========================
    print("\n===== ORIGINAL FEATURES =====")
    print(original_feature_names)

    print("\n===== SELECTED FEATURES =====")
    print(feature_names)

    print("\n===== UPLOADED FEATURES =====")
    print(list(df.columns))

    # =========================
    # House Price Dataset Fix
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

    if "street" in df.columns:

        df.drop(
            columns=["street"],
            inplace=True
        )

    # =========================
    # Loan Dataset Fix
    # =========================
    if "Dependents" in df.columns:

        df["Dependents"] = (
            df["Dependents"]
            .astype(str)
            .replace(
                {
                    "3": "3+",
                    "3.0": "3+"
                }
            )
        )

    # =========================
    # Validate Features
    # =========================
    missing_cols = (
        set(original_feature_names)
        - set(df.columns)
    )

    if missing_cols:

        raise Exception(
            f"""
Missing Required Columns

Required:
{original_feature_names}

Uploaded:
{list(df.columns)}

Missing:
{list(missing_cols)}
"""
        )

    # =========================
    # Keep Only Training Features
    # =========================
    df = df[original_feature_names]

    # =========================
    # Missing Value Handling
    # =========================
    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):

            df[col] = df[col].fillna(
                df[col].median()
            )

        else:

            df[col] = df[col].fillna(
                "Unknown"
            )

    # =========================
    # Encode Categories
    # =========================
    for col, encoder in feature_encoders.items():

        if col in df.columns:

            df[col] = df[col].astype(str)

            known_values = set(
                encoder.categories_[0]
            )

            df[col] = df[col].apply(
                lambda x:
                x if x in known_values
                else encoder.categories_[0][0]
            )

            df[[col]] = encoder.transform(
                df[[col]]
            )

    # =========================
    # Restore Original Feature Order
    # =========================
    df = df[original_feature_names]

    # =========================
    # Feature Selection
    # =========================
    df = pd.DataFrame(
        selector.transform(df),
        columns=feature_names
    )

    # =========================
    # Feature Scaling
    # =========================
    df = pd.DataFrame(
        scaler.transform(df),
        columns=feature_names
    )

    print("\n===== FINAL DATA =====")
    print(df.head())

    # =========================
    # Prediction
    # =========================
    predictions = model.predict(df)

    # =========================
    # Output
    # =========================
    if problem_type == "classification":

        df["Prediction"] = [
            "Approved"
            if p == 1
            else "Rejected"
            for p in predictions
        ]

    else:

        df["Prediction"] = np.round(
            predictions
        ).astype(int)

    return df