#!/usr/bin/env bash

IMAGE=joibel/argocd-plugin-helmfile-aas:latest
docker build . -t "${IMAGE}" && docker push "${IMAGE}"
