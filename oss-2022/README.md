# Automating Cloud-native Spark Jobs with Argo Workflows

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io?utm_campaign=talk-demos)

[The talk can be found here](https://www.youtube.com/watch?v=QV3YKUOiKo0).

## Goal of this repository
- Showcase how Spark Jobs can be orchestrated with Argo Workflows
- Provide a how-to steps to run all examples on local.

## Requirements
- k3d
- kubectl
- helm
- AWS account (used for second example)
- Kaggle account (used for second example)

## Infra setup
- Start a new kubernetes cluster (using k3d)
```
k3d cluster create
```
- Install Argo Workflows
```
kubectl create ns argo
kubectl -n argo apply -f infra/argo-install.yaml
```
- Install Spark k8s operator and add permission for Argo Workflows
```
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm install spark spark-operator/spark-operator --namespace spark-operator --create-namespace --set webhook.enable=true --set sparkJobNamespace=default --set serviceAccounts.spark.name=spark-driver
kubectl -n argo apply -f infra/argo-rbac.yaml
```

## Demo video
[View a recording of this demo on Google Drive here.](https://drive.google.com/file/d/1HH8oIf1keWXlmutlzcocC0_T-G0l5OJt/view?usp=sharing)

## How to build and run examples

### Scala example
Scala examples are located in scala folder. Examples are using dataset from `Kaggle.com`. Both examples are pretty basic, they are loading file from file system and are doing simple `reduceByKey` (summing number of rides per bike type and ride length by bike type).
These two examples are combined in simple Argo Workflow DAG and are running in parallel.
#### How to run Scala example
- Go to Scala folder
```
cd scala
```
- Build Docker image and import it to Kubernetes cluster
```
docker build -t argo-spark-integration-scala .
k3d image import argo-spark-integration-scala:latest
```
- Connect to Argo Workflows
```
kubectl -n argo port-forward deploy/argo-server 2746:2746
```
- Access Argo on `localhost:2746` (or using Argo CLI) and submit `workflow-scala.yaml`


### Python example
Python example is very similar to Scala example. The only difference is that we are not using dataset from local file system and are instead downloading from `Kaggle.com` and saving it to AWS S3. Everything else is similar to the previous example.
This example is creating `CronWorkflow` and it's requiring `Kaggle.com` and `AWS` account.

#### How to run Python example
- Go to Python folder
```
cd python
```
- Build and import Docker image.
```
docker build -t argo-spark-integration-python-download-job -f Dockerfile-python-download-job .
k3d image import argo-spark-integration-python-download-job:latest

docker build -t argo-spark-integration-python-bike-job -f Dockerfile-python-bike-job .
k3d image import argo-spark-integration-python-bike-job:latest
```
- Edit `workflow-python-config.yaml` and enter `awsRegion`, `awsBucketName` and `fileLocation`. After that add `ConfigMap` to cluster.
```
kubectl apply -f workflow-python-config.yaml -n argo
kubectl apply -f workflow-python-config.yaml -n default
```
- Edit `workflow-python-secrets.yaml` and enter `apiUser`, `apiPassword` (from `Keggle.com`), `awsAccessKeyId` and `awsSecretKey`. After that add `Secret` to cluster.
```
kubectl apply -f workflow-python-secrets.yaml -n argo
kubectl apply -f workflow-python-secrets.yaml -n default
```
- Connect to Argo Workflows
```
kubectl -n argo port-forward deploy/argo-server 2746:2746
```
- Access Argo on `localhost:2746` (or using Argo CLI) and submit `cron-workflow-python.yaml`

---

## About Pipekit

Pipekit is the control plane for Argo Workflows. Platform teams use Pipekit to manage data & CI pipelines at scale, while giving developers self-serve access to Argo. Pipekit's unified logging view, enterprise-grade RBAC, and multi-cluster management capabilities lower maintenance costs for platform teams while delivering a superior devex for Argo users. Sign up for a 30-day free trial at [pipekit.io/signup](https://pipekit.io/signup?utm_campaign=talk-demos).

Learn more about Pipekit's professional support for companies already using Argo at [pipekit.io/services](https://pipekit.io/services?utm_campaign=talk-demos).
