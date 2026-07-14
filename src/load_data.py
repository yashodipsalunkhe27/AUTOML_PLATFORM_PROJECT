import pandas as pd
import os


def load_dataset(path: str):
    """
    Load only structured dataset files.

    Supported formats:
    - CSV
    - Excel (.xlsx)
    - JSON

    TXT and dictionary-like inputs are NOT supported.
    """

    if not isinstance(path, str):
        raise ValueError("Invalid input: file path must be a string")

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    extension = os.path.splitext(path)[1].lower()

    if extension == ".csv":
        df = pd.read_csv(path)

    elif extension in [".xlsx", ".xls"]:
        df = pd.read_excel(path)

    elif extension == ".json":
        df = pd.read_json(path)

    else:
        raise ValueError(
            f"Unsupported dataset format: {extension}. "
            "Only CSV, Excel, and JSON files are allowed."
        )

    # =========================
    # VALIDATION (STRICT DATASET CHECK)
    # =========================

    if df is None or df.empty:
        raise ValueError("Dataset is empty")

    if len(df.columns) < 2:
        raise ValueError("Invalid dataset: must contain at least 2 columns")

    return df