import os
import shap
import matplotlib.pyplot as plt
import numpy as np


GRAPH_DIR = "graphs"


def generate_shap_summary(model, X_train):

    os.makedirs(GRAPH_DIR, exist_ok=True)

    try:

        # Use only first 100 rows
        sample = X_train.iloc[:100].copy()

        # Tree models
        explainer = shap.TreeExplainer(
            model,
            feature_perturbation="tree_path_dependent"
        )

        shap_values = explainer.shap_values(sample)

        plt.figure(figsize=(10,6))

        shap.summary_plot(
            shap_values,
            sample,
            show=False
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                GRAPH_DIR,
                "shap_summary.png"
            ),
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("SHAP Summary Generated Successfully")

    except Exception as e:

        print("SHAP ERROR :", e)