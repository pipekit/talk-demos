from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from numpy import ndarray
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_and_split_dataset(
    dataset_path: Path | str,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.Series,
    pd.Series,
]:
    data = pd.read_csv(dataset_path)

    X = data.drop("Outcome", axis=1)
    y = data["Outcome"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test


def feature_scaling(
    X_train: pd.DataFrame, X_test: pd.DataFrame
) -> tuple[ndarray, ndarray]:
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test


def model_training(X_train: ndarray, y_train: pd.Series) -> LogisticRegression:
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    return model


def make_predictions(model: LogisticRegression, X_test: ndarray) -> pd.DataFrame:
    y_pred = model.predict(X_test)
    return y_pred


def evaluate(
    model: LogisticRegression,
    X_test: ndarray,
    y_test: pd.Series,
    y_pred: ndarray,
) -> tuple[float, str]:
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    print(report)

    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)

    plot_path = "./roc_curve.png"
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {auc:.2f})")
    plt.plot([0, 1], [0, 1], "k--", label="Random Guessing")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()

    plt.savefig(plot_path)
    print(f"Plot at {plot_path}")

    plt.close()

    return accuracy, report


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = load_and_split_dataset("assets/diabetes.csv")
    X_train, X_test = feature_scaling(X_train, X_test)
    model = model_training(X_train, y_train)
    y_pred = make_predictions(model, X_test)
    accuracy, report = evaluate(model, X_test, y_test, y_pred)
