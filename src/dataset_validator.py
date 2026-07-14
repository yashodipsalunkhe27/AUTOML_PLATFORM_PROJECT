import pandas as pd
from fastapi import HTTPException


def validate_dataset(df, target_column):

    # =========================
    # Empty dataset
    # =========================
    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Dataset is empty."
        )

    # =========================
    # Only one column
    # =========================
    if df.shape[1] < 2:
        raise HTTPException(
            status_code=400,
            detail="Dataset must contain at least one feature and one target column."
        )

    # =========================
    # Duplicate column names
    # =========================
    duplicate_columns = df.columns[df.columns.duplicated()].tolist()

    if duplicate_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Duplicate column names found: {duplicate_columns}"
        )

    # =========================
    # Target exists
    # =========================
    if target_column not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Target column '{target_column}' not found."
        )

    # =========================
    # Empty target
    # =========================
    if df[target_column].isnull().all():
        raise HTTPException(
            status_code=400,
            detail="Target column contains only missing values."
        )

    # =========================
    # Constant target
    # =========================
    if df[target_column].nunique() < 2:
        raise HTTPException(
            status_code=400,
            detail="Target column must contain at least 2 unique values."
        )

    # =========================
    # All-null columns
    # =========================
    all_null_columns = [
        col for col in df.columns
        if df[col].isnull().all()
    ]

    if all_null_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Columns with all missing values: {all_null_columns}"
        )

    # =========================
    # Unsupported dtypes
    # =========================
    unsupported = []

    for col in df.columns:

        if pd.api.types.is_complex_dtype(df[col]):

            unsupported.append(col)

    if unsupported:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported data types found: {unsupported}"
        )

    # =========================
    # Duplicate rows (warning only)
    # =========================
    duplicate_rows = int(df.duplicated().sum())

    return {
        "duplicate_rows": duplicate_rows
    }