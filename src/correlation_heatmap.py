import matplotlib.pyplot as plt
import seaborn as sns
import os

GRAPH_DIR = "graphs"


def generate_correlation_heatmap(df):

    numeric_df = df.select_dtypes(include=["number"])

    correlation_matrix = numeric_df.corr()

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Correlation Heatmap")
    plt.tight_layout()

    save_path = os.path.join(
        GRAPH_DIR,
        "correlation_heatmap.png"
    )

    plt.savefig(save_path)
    plt.close()