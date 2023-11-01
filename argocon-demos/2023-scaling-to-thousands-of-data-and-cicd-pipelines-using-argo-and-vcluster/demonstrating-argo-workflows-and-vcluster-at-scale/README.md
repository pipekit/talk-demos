# Demonstrating Argo Workflows and vCluster at scale

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io)

This represents a somewhat unrealistic scenario where you may want to run a 'hello world' workflow 12000 times as fast as possible!
The workflow is a simple hello world workflow that runs a single container that prints 'hello world' to the logs.... 400 times per vcluster. We recommend you swap the 'hello world' workflow for something more realistic to your needs.

**This will run 12000+ pods in as short a space of time as possible. It's expensive to run. You are very likely to max out your etcd database and breach Kubernetes API limits.**

The aim of this is to demonstrate that by running many Argo Workflows instances inside vClusters, you will reduce the number of API calls made back to the kubernetes API on the host cluster. This will reduce API throttling and should allow you to run more workflows/pods concurrently than you would if you were just running on the host cluster.

## Prepare the vClusters
We used [vCluster pro](https://www.vcluster.com/pro/) for this test. This allows us to use CRs to create the vclusters, instead of the full helm chart.

You will first need to create and deploy a `VirtualClusterTemplate` CR. One is not supplied here as the exact template will depend on your needs.

### Log into vcluster:

```bash
vcluster login https://your-vcluster-pro-url.biz
```

### Create the clusters

```bash
for ns in load0 load1 load2 load3 load4 load5 load6 load7 load8 load9 load10 load11 load12 load13 load14 load15 load16 load17 load18 load19 load20 load21 load22 load23 load24 load25 load26 load27 load28 load29 load30; do
    helm template -n loft-p-default load vcluster-pro-manifest -f vcluster-pro-manifest-helm/values.yaml --set vcid=$ns | kubectl apply --wait=false -f -
done
```

### Install Argo Workflows into each cluster
```bash
for ns in load0 load1 load2 load3 load4 load5 load6 load7 load8 load9 load10 load11 load12 load13 load14 load15 load16 load17 load18 load19 load20 load21 load22 load23 load24 load25 load26 load27 load28 load29 load30; do
    vcluster connect $ns
	kubectl create namespace argo || true
	kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.5.0/install.yaml
    vcluster disconnect
done
```

## Start the Test
```bash
for ns in load0 load1 load2 load3 load4 load5 load6 load7 load8 load9 load10 load11 load12 load13 load14 load15 load16 load17 load18 load19 load20 load21 load22 load23 load24 load25 load26 load27 load28 load29 load30; do
    vcluster connect $ns
	kubectl create -n argo -f lots-of-hellos-workflow.yaml
    vcluster disconnect
done

```

## Delete the vclusters
```bash
for ns in load0 load1 load2 load3 load4 load5 load6 load7 load8 load9 load10 load11 load12 load13 load14 load15 load16 load17 load18 load19 load20 load21 load22 load23 load24 load25 load26 load27 load28 load29 load30; do
    helm template -n loft-p-default load vcluster-pro-manifest -f vcluster-pro-manifest/values.yaml --set vcid=$ns | kubectl delete --wait=false -f - || true
done

```
