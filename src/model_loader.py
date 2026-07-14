import joblib
import os

MODEL_PATH = "models/production/best_model.pkl"

def load_model():

    if not os.path.exists(MODEL_PATH):
        raise Exception(
            f"Model not found at {MODEL_PATH}. Please train the model first."
        )

    return joblib.load(MODEL_PATH)