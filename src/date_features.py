import pandas as pd

def create_date_features(df):

    for col in df.columns:

        if "date" in col.lower():

            try:

                df[col] = pd.to_datetime(
                    df[col],
                    errors="coerce"
                )

                df[f"{col}_year"] = \
                    df[col].dt.year

                df[f"{col}_month"] = \
                    df[col].dt.month

                df[f"{col}_day"] = \
                    df[col].dt.day

                df[f"{col}_weekday"] = \
                    df[col].dt.weekday

                df.drop(
                    columns=[col],
                    inplace=True
                )

            except:
                pass

    return df