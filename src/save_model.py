import joblib

def save_model(model):

    joblib.dump(
        model,
        "models/loan_model.pkl"
    )

    print("Model Saved Successfully")