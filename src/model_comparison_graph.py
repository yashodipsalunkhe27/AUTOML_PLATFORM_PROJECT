import joblib
import matplotlib.pyplot as plt


def generate_model_comparison_graph():

    results = joblib.load("models/model_results.pkl")

    models = list(results.keys())

    scores = [
        results[model]["score"] * 100
        for model in models
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(models, scores)

    plt.title("Model Score Comparison")
    plt.xlabel("Models")
    plt.ylabel("Score (%)")

    plt.xticks(rotation=20)

    plt.tight_layout()

    plt.savefig("graphs/model_comparison.png")

    plt.close()