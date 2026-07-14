import os
import joblib

ARTIFACT_DIR = "models/artifacts"
ENCODER_DIR = "models/encoders"


def get_prediction_schema():

    original_features = joblib.load(
        os.path.join(
            ARTIFACT_DIR,
            "original_feature_names.pkl"
        )
    )

    feature_encoders = joblib.load(
        os.path.join(
            ENCODER_DIR,
            "feature_encoders.pkl"
        )
    )

    schema = {}

    for feature in original_features:

        if feature in feature_encoders:

            schema[feature] = "string"

        else:

            schema[feature] = "number"

    return schema