from sklearn.model_selection import train_test_split
from pandas.api.types import is_numeric_dtype


def split_dataset(df, target_column):

    X = df.drop(columns=[target_column])
    y = df[target_column]

    stratify = None

    if (
        not is_numeric_dtype(y)
        or y.nunique() <= 20
    ):
        stratify = y if y.nunique() <= 20 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=stratify
    )

    return X_train, X_test, y_train, y_test