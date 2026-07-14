import pandas as pd
from pandas.api.types import is_numeric_dtype

def handle_missing_values(df):
    """
    Fill missing values:
    - Numerical columns -> median
    - Categorical/String columns -> mode
    """

    for col in df.columns:

        # Skip columns with no missing values
        if not df[col].isnull().any():
            continue

        # Numerical columns
        if is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())

        # Categorical/String columns
        else:
            mode_value = df[col].mode()

            if not mode_value.empty:
                df[col] = df[col].fillna(mode_value[0])
            else:
                df[col] = df[col].fillna("Unknown")

    return df