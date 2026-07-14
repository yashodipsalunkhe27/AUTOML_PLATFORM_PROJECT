import os
import joblib
import numpy as np

from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    roc_auc_score,
    matthews_corrcoef,
    cohen_kappa_score,
    confusion_matrix,
    classification_report,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def evaluate_model(
    model,
    X_test,
    y_test,
    problem_type="classification"
):

    # ==========================
    # Prediction
    # ==========================
    y_pred = model.predict(X_test)

    y_prob = None

    if (
        problem_type == "classification"
        and hasattr(model, "predict_proba")
    ):
        y_prob = model.predict_proba(X_test)

    # ==========================
    # Label Encoding Fix
    # ==========================
    if problem_type == "classification":

        if y_test.dtype != y_pred.dtype:

            le = LabelEncoder()

            le.fit(
                np.concatenate(
                    [
                        y_test.astype(str),
                        y_pred.astype(str)
                    ]
                )
            )

            y_test = le.transform(
                y_test.astype(str)
            )

            y_pred = le.transform(
                y_pred.astype(str)
            )

    # =====================================================
    # CLASSIFICATION
    # =====================================================
    if problem_type == "classification":

        accuracy = accuracy_score(
            y_test,
            y_pred
        )

        balanced_accuracy = balanced_accuracy_score(
            y_test,
            y_pred
        )

        mcc = matthews_corrcoef(
            y_test,
            y_pred
        )

        kappa = cohen_kappa_score(
            y_test,
            y_pred
        )

        cm = confusion_matrix(
            y_test,
            y_pred
        )

        classification = classification_report(
            y_test,
            y_pred,
            output_dict=True,
            zero_division=0
        )

        # ----------------------------
        # ROC AUC
        # ----------------------------
        roc_auc = None

        if (
            y_prob is not None
            and len(np.unique(y_test)) == 2
        ):
            roc_auc = round(
                roc_auc_score(
                    y_test,
                    y_prob[:, 1]
                ),
                4
            )

        # ----------------------------
        # Convert labels back
        # ----------------------------
        encoder_path = "models/encoders/target_encoder.pkl"

        if os.path.exists(encoder_path):

            target_encoder = joblib.load(
                encoder_path
            )

            if target_encoder is not None:

                class_mapping = {

                    str(i): str(label)

                    for i, label in enumerate(
                        target_encoder.classes_
                    )

                }

                new_report = {}

                for key, value in classification.items():

                    if key in class_mapping:
                        new_report[class_mapping[key]] = value
                    else:
                        new_report[key] = value

                classification = new_report

        report = {

            "accuracy": round(
                accuracy,
                4
            ),

            "balanced_accuracy": round(
                balanced_accuracy,
                4
            ),

            "precision": round(
                classification["weighted avg"]["precision"],
                4
            ),

            "recall": round(
                classification["weighted avg"]["recall"],
                4
            ),

            "f1_score": round(
                classification["weighted avg"]["f1-score"],
                4
            ),

            "mcc": round(
                mcc,
                4
            ),

            "kappa": round(
                kappa,
                4
            ),

            "roc_auc": roc_auc,

            "classification_report": classification
        }

        return accuracy, cm, report

    # =====================================================
    # REGRESSION
    # =====================================================

    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    mse = mean_squared_error(
        y_test,
        y_pred
    )

    rmse = np.sqrt(mse)

    r2 = r2_score(
        y_test,
        y_pred
    )

    report = {

        "MAE": round(
            mae,
            4
        ),

        "MSE": round(
            mse,
            4
        ),

        "RMSE": round(
            rmse,
            4
        ),

        "R2": round(
            r2,
            4
        )

    }

    return r2, None, report