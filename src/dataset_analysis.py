import pandas as pd
import os
import joblib


def analyze_dataset(df):

    # -----------------------
    # TARGET COLUMN
    # -----------------------
    TARGET_PATH = "models/artifacts/target_column.pkl"

    target_column = None
    feature_df = df.copy()

    # Load target column only if it exists AND belongs to the current dataset
    if os.path.exists(TARGET_PATH):
        saved_target = joblib.load(TARGET_PATH)

        if saved_target in df.columns:
            target_column = saved_target
            feature_df = df.drop(columns=[saved_target])

    # -----------------------
    # 1. ID Columns Detection
    # -----------------------
    id_columns = []

    for col in feature_df.columns:
        if "id" in col.lower():
            id_columns.append(col)

    # -----------------------
    # 2. Categorical Columns
    # -----------------------
    categorical_columns = (
        feature_df.select_dtypes(include=["object"])
        .columns
        .tolist()
    )

    # Remove ID columns
    categorical_columns = [
        col for col in categorical_columns
        if col not in id_columns
    ]

    # -----------------------
    # 3. Numerical Columns
    # -----------------------
    numerical_columns = (
        feature_df.select_dtypes(include=["int64", "float64"])
        .columns
        .tolist()
    )

    # Remove ID columns
    numerical_columns = [
        col for col in numerical_columns
        if col not in id_columns
    ]

    # -----------------------
    # 4. Constant Columns
    # -----------------------
    constant_columns = [
        col
        for col in feature_df.columns
        if feature_df[col].nunique(dropna=False) <= 1
    ]

    # -----------------------
    # 5. Duplicate Rows
    # -----------------------
    duplicate_rows = int(df.duplicated().sum())

    # -----------------------
    # 6. Return Result
    # -----------------------
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),

        "target_column": target_column,

        "id_columns": id_columns,
        "categorical_columns": categorical_columns,
        "numerical_columns": numerical_columns,

        "constant_columns": constant_columns,
        "duplicate_rows": duplicate_rows,

        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict()
    }