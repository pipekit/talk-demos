"""A workflow to run model training and evaluation.

It uses the "script_annotations" feature to allow a more Pythonic developer experience.
It can be run on a local docker desktop installation of Argo Workflows using `make run`. The
environment setup can be done with `make install-environment` which installs argo and minio.

Note that:
* You must port-forward the Argo service
* There must be a `workflows` bucket on minio with the `diabetes.csv` file in it
    * You must also port-forward the minio service
    * Then, you can use the minio client to run
```
mc alias set localminio http://localhost:9000 argoproj sup3rs3cr3tp4ssw0rd1
mc mb localminio/workflows
mc put assets/diabetes.csv localminio/workflows/diabetes.csv
```
"""

import os
import pickle
from pathlib import Path
from typing import Annotated

import hera.workflows.models as m
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from hera.shared import global_config
from hera.workflows import (
    DAG,
    Artifact,
    ArtifactLoader,
    NoneArchiveStrategy,
    Parameter,
    RunnerScriptConstructor,
    S3Artifact,
    Script,
    Workflow,
    script,
)
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

global_config.image = os.environ.get("IMAGE_NAME") or "ds-blog:v1"
global_config.experimental_features["script_annotations"] = True

global_config.set_class_defaults(Script, constructor=RunnerScriptConstructor())


# Load dataset
@script()
def load_and_split_dataset(
    dataset_path: Annotated[
        Path,
        S3Artifact(
            name="dataset-path",
            endpoint="minio:9000",
            bucket="workflows",
            key="diabetes.csv",
            access_key_secret=m.SecretKeySelector(
                name="my-minio-cred",
                key="accesskey",
            ),
            secret_key_secret=m.SecretKeySelector(
                name="my-minio-cred",
                key="secretkey",
            ),
            insecure=True,
            loader=None,
        ),
    ],
) -> tuple[
    Annotated[str, Artifact(name="X_train", archive=NoneArchiveStrategy())],
    Annotated[str, Artifact(name="X_test", archive=NoneArchiveStrategy())],
    Annotated[str, Artifact(name="y_train", archive=NoneArchiveStrategy())],
    Annotated[str, Artifact(name="y_test", archive=NoneArchiveStrategy())],
]:
    data = pd.read_csv(dataset_path)

    # Split into features and target
    X = data.drop("Outcome", axis=1)
    y = data["Outcome"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    assert isinstance(X_train, pd.DataFrame), type(X_train)
    assert isinstance(X_test, pd.DataFrame), type(X_test)
    assert isinstance(y_train, pd.Series), type(y_train)
    assert isinstance(y_test, pd.Series), type(y_test)

    return (
        X_train.to_json(),
        X_test.to_json(),
        y_train.to_json(),
        y_test.to_json(),
    )


@script()
def feature_scaling(
    X_train: Annotated[dict, Artifact(name="X_train", loader=ArtifactLoader.json)],
    X_test: Annotated[dict, Artifact(name="X_test", loader=ArtifactLoader.json)],
) -> tuple[
    Annotated[list, Artifact(name="X_train", archive=NoneArchiveStrategy())],
    Annotated[list, Artifact(name="X_test", archive=NoneArchiveStrategy())],
]:
    scaler = StandardScaler()
    X_train = scaler.fit_transform(pd.DataFrame.from_dict(X_train))
    X_test = scaler.transform(pd.DataFrame.from_dict(X_test))
    assert isinstance(X_train, ndarray), type(X_train)
    assert isinstance(X_test, ndarray), type(X_test)
    return (X_train.tolist(), X_test.tolist())


@script()
def model_training(
    X_train: Annotated[list, Artifact(name="X_train", loader=ArtifactLoader.json)],
    y_train: Annotated[dict, Artifact(name="y_train", loader=ArtifactLoader.json)],
    model_path: Annotated[
        Path, Artifact(name="model", archive=NoneArchiveStrategy(), output=True)
    ],
):
    X_train = np.array(X_train)
    y_train = pd.Series(y_train)
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    model_path.write_bytes(pickle.dumps(model))


@script()
def make_predictions(
    model_path: Annotated[Path, Artifact(name="model", loader=None)],
    X_test_list: Annotated[list, Artifact(name="X_test", loader=ArtifactLoader.json)],
) -> Annotated[list, Artifact(name="y_pred", archive=NoneArchiveStrategy())]:
    model = pickle.loads(model_path.read_bytes())
    X_test = np.array(X_test_list)
    assert isinstance(model, LogisticRegression), type(model)
    assert isinstance(X_test, np.ndarray), type(X_test)
    y_pred = model.predict(X_test)
    return y_pred.tolist()


@script()
def evaluate(
    model_path: Annotated[Path, Artifact(name="model", loader=None)],
    X_test_list: Annotated[list, Artifact(name="X_test", loader=ArtifactLoader.json)],
    y_test_list: Annotated[dict, Artifact(name="y_test", loader=ArtifactLoader.json)],
    y_pred_list: Annotated[list, Artifact(name="y_pred", loader=ArtifactLoader.json)],
    plot_path: Annotated[
        Path,
        Artifact(
            name="plot",
            path="/tmp/roc_curve.png",
            output=True,
            archive=NoneArchiveStrategy(),
        ),
    ],
    report_path: Annotated[
        Path,
        Artifact(
            name="report",
            path="/tmp/report.txt",
            output=True,
            archive=NoneArchiveStrategy(),
        ),
    ],
) -> Annotated[float, Parameter(name="accuracy")]:
    model = pickle.loads(model_path.read_bytes())
    X_test = np.array(X_test_list)
    y_test = pd.Series(y_test_list)
    y_pred = np.array(y_pred_list)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    report_path.write_text(report)

    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {auc:.2f})")
    plt.plot([0, 1], [0, 1], "k--", label="Random Guessing")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()

    plt.savefig(str(plot_path))

    plt.close()

    return accuracy


with Workflow(
    generate_name="model-training-pipeline-",
    entrypoint="run-training",
) as w:
    with DAG(name="run-training"):
        datasets_task = load_and_split_dataset()
        scaling_task = feature_scaling(
            arguments=[
                datasets_task.get_artifact("X_train"),
                datasets_task.get_artifact("X_test"),
            ]
        )
        model_training_task = model_training(
            arguments=[
                scaling_task.get_artifact("X_train"),
                datasets_task.get_artifact("y_train"),
            ]
        )

        make_predictions_task = make_predictions(
            arguments=[
                model_training_task.get_artifact("model"),
                scaling_task.get_artifact("X_test"),
            ]
        )

        evaluate_task = evaluate(
            arguments=[
                model_training_task.get_artifact("model"),
                scaling_task.get_artifact("X_test"),
                datasets_task.get_artifact("y_test"),
                make_predictions_task.get_artifact("y_pred"),
            ]
        )

        (
            datasets_task
            >> scaling_task
            >> model_training_task
            >> make_predictions_task
            >> evaluate_task
        )
