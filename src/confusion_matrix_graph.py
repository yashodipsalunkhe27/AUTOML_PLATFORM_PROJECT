import matplotlib.pyplot as plt

def generate_confusion_matrix_graph(cm):

    plt.figure(figsize=(5, 4))

    plt.imshow(cm)

    plt.title("Confusion Matrix")

    plt.colorbar()

    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.tight_layout()

    plt.savefig(
        "graphs/confusion_matrix.png"
    )

    plt.close()