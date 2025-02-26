#!/usr/bin/env bash

k3d cluster delete template-examples || true
k3d cluster create --config bootstrap/k3d.conf

# Prevent users from accidentally deploying to the wrong cluster.
currentContext=$(kubectl config current-context)
if [ "$currentContext" == "k3d-template-examples" ]; then
    echo "Starting deployment to cluster..."
else
    echo "The kubectl context is not what we expected. Exiting for safety. Perhaps the k3d cluster failed to create?"
    exit 1
fi

# Deploy Argo Workflows
while ! kubectl get nodes > /dev/null 2>&1; do sleep 1; done
kubectl create ns argo || true
kubectl -n argo apply -k bootstrap/argo-workflows
kubectl create ns workflows || true
kubectl -n workflows apply -f bootstrap/argo-workflows/wf-sa.yaml
kubectl -n workflows apply -k bootstrap/plugin

kubectl wait -n argo deploy/argo-server --for condition=Available --timeout 2m >/dev/null
kubectl wait -n argo deploy/workflow-controller --for condition=Available --timeout 2m >/dev/null

# Port-forward the Argo Server in the background
kubectl -n argo port-forward svc/argo-server 2746:2746 > /dev/null 2>&1 &
echo "############################################"
echo "############################################"
echo "Argo Server is available at https://localhost:2746/workflows/workflows?&limit=50 (accept the self-signed certificate)"
echo "############################################"
echo "############################################"
