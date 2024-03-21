#!/usr/bin/env bash

kubectl create ns argocd
kustomize build | kubectl apply -f -
kubens argocd
sleep 60
argocd admin initial-password reset
kubectl port-forward svc/argocd-server -n argocd 8080:443
