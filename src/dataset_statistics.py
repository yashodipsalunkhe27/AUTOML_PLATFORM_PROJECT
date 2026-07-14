def get_dataset_statistics(df):

    return {
        "describe": df.describe(include="all").fillna("").to_dict(),
        "shape": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1])
        }
    }