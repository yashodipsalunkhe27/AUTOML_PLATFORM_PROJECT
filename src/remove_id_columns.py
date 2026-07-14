def remove_id_columns(df):

    id_columns = []

    for col in df.columns:

        if "id" in col.lower():
            id_columns.append(col)

    if len(id_columns) > 0:
        df = df.drop(columns=id_columns)

    return df