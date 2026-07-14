def remove_constant_columns(df):

    constant_cols = []

    for col in df.columns:

        if df[col].nunique() <= 1:
            constant_cols.append(col)

    if len(constant_cols) > 0:
        df = df.drop(columns=constant_cols)

    return df, constant_cols