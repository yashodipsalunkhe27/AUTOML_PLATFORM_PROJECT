import os
import json

HISTORY_FILE = "models/training_history.json"


def save_training_history(record):

    os.makedirs("models", exist_ok=True)

    history = []

    if os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except:
                history = []

    history.append(record)

    with open(HISTORY_FILE, "w") as f:
        json.dump(
            history,
            f,
            indent=4
        )


def get_training_history(limit=None, page=1):

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    # Show latest training first
    history.reverse()

    if limit is None:
        return history

    start = (page - 1) * limit
    end = start + limit

    return history[start:end]