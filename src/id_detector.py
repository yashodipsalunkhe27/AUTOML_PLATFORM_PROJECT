def detect_high_cardinality(df):

    high_card_cols = []

    categorical_cols = df.select_dtypes(
        include=["object"]
    ).columns

    for col in categorical_cols:

        if df[col].nunique() > 100:

            high_card_cols.append(col)

    return high_card_cols