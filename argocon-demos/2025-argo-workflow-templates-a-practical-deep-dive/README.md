# Argo Workflow Templtes: A Practical Deep Dive

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io?utm_campaign=talk-demos)


## The talk
<!--
The talk recording [can be found here](https://youtu.be/grDJ3o2VLUE).
-->
The slide deck for this talk can be found [here](assets/slide-deck.pdf).

## Examples

We have created a series of example workflows that uses each of the templates we discussed in the talk. They are packaged up in to a k3d cluster so you can run locally and experiment:

### Prerequisites
1. [k3d](https://k3d.io/#installation) installed

### Installation
1. Navigate to the `examples` directory
1. Run `./setup.sh` to install the k3d cluster and the Argo Workflows.
1. When prompted, you can navigate to the Argo UI by clicking on the link provided (remember to accept the self-signed certificate).

### Running the Examples
1. Navigate to the `examples/template-examples` directory
1. Apply each of the examples by running `kubectl -n workflows create -f <example>.yaml`
1. Observe the outcome in the Workflows UI.

### Cleanup
To remove the k3d cluster and the Argo Workflows, run `k3d cluster delete template-examples`.
---

## About Pipekit

Pipekit is the control plane for Argo Workflows. Platform teams use Pipekit to manage data & CI pipelines at scale, while giving developers self-serve access to Argo. Pipekit's unified logging view, Workflow Metrics dashboards, enterprise-grade RBAC and multi-cluster management capabilities lower maintenance costs for platform teams while delivering a superior devex for Argo users. Sign up for a 30-day free trial at [pipekit.io/signup](https://pipekit.io/signup?utm_campaign=talk-demos).

Learn more about Pipekit's professional support for companies already using Argo at [pipekit.io/services](https://pipekit.io/services?utm_campaign=talk-demos).
