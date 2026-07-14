import os
import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler

ENCODER_DIR = "models/encoders"


def scale_features(X):

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    joblib.dump(
        scaler,
        os.path.join(
            ENCODER_DIR,
            "scaler.pkl"
        )
    )

    return pd.DataFrame(
        X_scaled,
        columns=X.columns,
        index=X.index
    )