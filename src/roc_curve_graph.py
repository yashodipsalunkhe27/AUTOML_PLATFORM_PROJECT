import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import (
    roc_curve,
    auc
)

from sklearn.preprocessing import LabelEncoder

GRAPH_DIR = "graphs"


def generate_roc_curve(
    y_test,
    y_probs
):
    """
    Generate ROC curve for binary classification.
    Automatically converts string labels to integers.
    """

    # =========================
    # Convert to NumPy arrays
    # =========================
    y_test = np.asarray(y_test)
    y_probs = np.asarray(y_probs)

    # =========================
    # Encode string labels
    # =========================
    if y_test.dtype.kind in ("U", "S", "O"):

        encoder = LabelEncoder()

        y_test = encoder.fit_transform(y_test)

    # =========================
    # Flatten arrays
    # =========================
    y_test = y_test.ravel()
    y_probs = y_probs.ravel()

    # =========================
    # ROC Curve
    # =========================
    fpr, tpr, _ = roc_curve(
        y_test,
        y_probs,
        pos_label=1
    )

    roc_auc = auc(
        fpr,
        tpr
    )

    # =========================
    # Plot
    # =========================
    plt.figure(figsize=(8, 6))

    plt.plot(
        fpr,
        tpr,
        linewidth=2,
        label=f"AUC = {roc_auc:.4f}"
    )

    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--",
        linewidth=1
    )

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")

    os.makedirs(
        GRAPH_DIR,
        exist_ok=True
    )

    plt.savefig(
        os.path.join(
            GRAPH_DIR,
            "roc_curve.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()