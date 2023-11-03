# Scaling to Thousands of Data and CI/CD Pipelines using Argo and Virtual Clusters

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io?utm_campaign=talk-demos)

## The talk
<!-- The talk [can be found here](https://www.youtube.com/watch?v=QZI-LXJGWYI). -->

The slide deck for this talk can be found [here](assets/slide-deck.pdf).

## Example Workflow
An example workflow that demonstrates how you could use Argo Workflows and Argo CD to deploy and configure vClusters. It can be found [here](create-and-setup-vcluster-workflow/create.yaml).

## Demonstrating vCluster at scale
This is a very unscientific demonstration of how you could use vCluster at scale to eek out more performance from your existing cluster. It can be found [here](demonstrating-argo-workflows-and-vcluster-at-scale/README.md).

By running many Argo Workflows instances inside vClusters, you will reduce the number of API calls made back to the kubernetes API on the host cluster. This will reduce API throttling and should allow you to run more workflows/pods concurrently than you would if you were just running on the host cluster.

---

## About Pipekit

Pipekit is the control plane for Argo Workflows. Platform teams use Pipekit to manage data & CI pipelines at scale, while giving developers self-serve access to Argo. Pipekit's unified logging view, enterprise-grade RBAC, and multi-cluster management capabilities lower maintenance costs for platform teams while delivering a superior devex for Argo users. Sign up for a 30-day free trial at [pipekit.io/signup](https://pipekit.io/signup?utm_campaign=talk-demos).

Learn more about Pipekit's professional support for companies already using Argo at [pipekit.io/services](https://pipekit.io/services?utm_campaign=talk-demos).
