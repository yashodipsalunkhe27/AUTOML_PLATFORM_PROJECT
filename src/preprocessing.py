from sklearn.preprocessing import (
    OrdinalEncoder,
    LabelEncoder
)
from sklearn.impute import SimpleImputer
import pandas as pd

target_encoder = None
feature_encoders = {}


def remove_outliers(df, target_column):

    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    numeric_cols = [
        col for col in numeric_cols
        if col != target_column
    ]

    for col in numeric_cols:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df = df[
            (df[col] >= lower)
            &
            (df[col] <= upper)
        ]

    return df


def preprocess_data(df, target_column):

    global target_encoder
    global feature_encoders

    feature_encoders = {}
    target_encoder = None

    # ======================
    # Drop Loan_ID
    # ======================
    if "Loan_ID" in df.columns:
        df = df.drop(columns=["Loan_ID"])

    # ======================
    # Date Processing
    # ======================
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

    # ======================
    # Remove High Cardinality
    # ======================
    if "street" in df.columns:

        if df["street"].nunique() > 100:

            print("Dropping street column (high cardinality)")

            df.drop(
                columns=["street"],
                inplace=True
            )

    # ======================
    # Fill Numeric Missing Values
    # ======================
    num_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    num_imputer = SimpleImputer(
        strategy="median"
    )

    df[num_cols] = num_imputer.fit_transform(
        df[num_cols]
    )

    # ======================
    # Fill Categorical Missing Values
    # ======================
    cat_cols = df.select_dtypes(
        include=["object"]
    ).columns

    if len(cat_cols) > 0:

        cat_imputer = SimpleImputer(
            strategy="most_frequent"
        )

        df[cat_cols] = cat_imputer.fit_transform(
            df[cat_cols]
        )

    # ======================
    # Encode Target
    # ======================
    from pandas.api.types import is_numeric_dtype

    if not is_numeric_dtype(df[target_column]):

        target_encoder = LabelEncoder()

        df[target_column] = target_encoder.fit_transform(
            df[target_column].astype(str)
        )

        df[target_column] = df[target_column].astype(int)

    else:
        target_encoder = None

    # ======================
    # Encode Features
    # ======================
    categorical_cols = df.select_dtypes(
        include=["object"]
    ).columns

    for col in categorical_cols:

        if col == target_column:
            continue

        encoder = OrdinalEncoder(
            handle_unknown="use_encoded_value",
            unknown_value=-1
        )

        df[[col]] = encoder.fit_transform(
            df[[col]].astype(str)
        )

        feature_encoders[col] = encoder

    # ======================
    # Remove Outliers
    # ======================
    # df = remove_outliers(
    #     df,
    #     target_column
    # )

    print("\n===== AFTER PREPROCESSING =====")
    print(df.dtypes)

    return df