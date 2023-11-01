# Scaling to Thousands of Data and CI/CD Pipelines using Argo and Virtual Clusters

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io)

## The talk
<!-- The talk [can be found here](https://www.youtube.com/watch?v=QZI-LXJGWYI). -->

The slide deck for this talk can be found [here](assets/slide-deck.pdf).

## Example Workflow
An example workflow that demonstrates how you could use Argo Workflows and Argo CD to deploy and configure vClusters. It can be found [here](create-and-setup-vcluster-workflow/create.yaml).

## Demonstrating vCluster at scale
This is a very unscientific demonstration of how you could use vCluster at scale to eek out more performance from your existing cluster. It can be found [here](demonstrating-argo-workflows-and-vcluster-at-scale/README.md).

By running many Argo Workflows instances inside vClusters, you will reduce the number of API calls made back to the kubernetes API on the host cluster. This will reduce API throttling and should allow you to run more workflows/pods concurrently than you would if you were just running on the host cluster.

## Argo Workflows Support

For more information about Argo Workflows, please see the following resources:


* [The Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)
* [The Argo Workflows GitHub Repository](https://github.com/argoproj/argo-workflows/)
* [The Argo Workflows Slack Channel](https://cloud-native.slack.com/archives/C01QW9QSSSK)

---

## About Pipekit
[Pipekit](pipekit.io) allows you to manage your workflows at scale. The control plane configures Argo Workflows for you in your infrastructure, enabling you to optimize multi-cluster workloads while reducing your cloud spend.  The team at Pipekit is also happy to support you through your Argo Workflows journey via commercial support.
