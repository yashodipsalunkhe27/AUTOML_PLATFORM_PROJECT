def remove_duplicate_rows(df):
    original_rows = len(df)

    df = df.drop_duplicates()

    removed_rows = original_rows - len(df)

    return df, removed_rows