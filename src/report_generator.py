import os
import joblib

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet

MODEL_DIR = "models"
GRAPH_DIR = "graphs"
ARTIFACT_DIR = "models/artifacts"


def generate_training_report(dataset_name, rows, columns):

    os.makedirs("reports", exist_ok=True)

    pdf_path = "reports/Training_Report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    # =========================
    # TITLE
    # =========================
    story.append(
        Paragraph(
            "<b>AutoML Training Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # =========================
    # DATASET
    # =========================
    story.append(
        Paragraph(
            f"<b>Dataset:</b> {dataset_name}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Rows:</b> {rows}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Columns:</b> {columns}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 15))

    # =========================
    # MODEL INFO
    # =========================
    model = joblib.load(
        os.path.join(
            MODEL_DIR,
            "model_name.pkl"
        )
    )

    score = joblib.load(
        os.path.join(
            MODEL_DIR,
            "model_score.pkl"
        )
    )

    params = joblib.load(
        os.path.join(
            MODEL_DIR,
            "best_params.pkl"
        )
    )

    story.append(
        Paragraph(
            f"<b>Best Model:</b> {model}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Score:</b> {score}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Parameters:</b> {params}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # =========================
    # ADD GRAPHS
    # =========================
    graph_files = [

        "model_comparison.png",

        "confusion_matrix.png",

        "roc_curve.png",

        "feature_importance.png"

    ]

    for graph in graph_files:

        graph_path = os.path.join(
            GRAPH_DIR,
            graph
        )

        if os.path.exists(graph_path):

            story.append(
                Paragraph(
                    f"<b>{graph}</b>",
                    styles["Heading2"]
                )
            )

            story.append(
                Image(
                    graph_path,
                    width=400,
                    height=250
                )
            )

            story.append(
                Spacer(1, 20)
            )

    doc.build(story)

    return pdf_path