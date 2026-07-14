import matplotlib.pyplot as plt
import os

GRAPH_DIR = "graphs"

def generate_target_distribution(df, target_column):

    plt.figure(figsize=(6,4))

    df[target_column].value_counts().plot(
        kind="bar"
    )

    plt.title("Target Distribution")
    plt.tight_layout()

    save_path = os.path.join(
        GRAPH_DIR,
        "target_distribution.png"
    )

    plt.savefig(save_path)

    plt.close()