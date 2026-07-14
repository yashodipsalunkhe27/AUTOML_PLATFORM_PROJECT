import os
import joblib

ARTIFACT_DIR = "models/artifacts"


def get_dataset_summary(df):

    target = None
    problem_type = None

    target_path = os.path.join(
        ARTIFACT_DIR,
        "target_column.pkl"
    )

    problem_path = os.path.join(
        ARTIFACT_DIR,
        "problem_type.pkl"
    )

    if os.path.exists(target_path):
        target = joblib.load(target_path)

    if os.path.exists(problem_path):
        problem_type = joblib.load(problem_path)

    return {

        "rows": int(df.shape[0]),

        "columns": int(df.shape[1]),

        "target": target,

        "problem_type": problem_type,

        "duplicates": int(df.duplicated().sum()),

        "missing_values": int(df.isnull().sum().sum())
    }