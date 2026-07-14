import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_confusion_matrix(cm):

    # Create graphs folder automatically
    os.makedirs("graphs", exist_ok=True)

    plt.figure(figsize=(6, 5))

    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues'
    )

    plt.title("Confusion Matrix")

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    plt.savefig(
        "graphs/confusion_matrix.png"
    )

    plt.close()