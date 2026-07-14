from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder


def train_model(
    model,
    X_train,
    y_train
):

    if isinstance(model, XGBClassifier):

        encoder = LabelEncoder()

        y_train = encoder.fit_transform(y_train)

    model.fit(
        X_train,
        y_train
    )

    return model