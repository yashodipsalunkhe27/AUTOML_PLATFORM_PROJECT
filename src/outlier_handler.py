import pandas as pd


def remove_target_outliers(
    df,
    target_column
):

    if target_column not in df.columns:
        return df

    if not pd.api.types.is_numeric_dtype(
        df[target_column]
    ):
        return df

    q1 = df[target_column].quantile(0.25)

    q3 = df[target_column].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr

    upper = q3 + 1.5 * iqr

    df = df[
        (df[target_column] >= lower)
        &
        (df[target_column] <= upper)
    ]

    return df