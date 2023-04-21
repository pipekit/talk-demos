# Managing Artifacts at Scale for CI and Data Processing

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io)

## The talk
The talk [can be found here](https://youtu.be/ucnOQuNkIbE).

## Workflow configuration & setup
The workflow controller configmap configuration we used is in this repo. However, more information on setting up an S3 artifact repository with Argo Workflows can be found in the [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/configure-artifact-repository/#configuring-aws-s3)

## Working examples using S3
Visit [this CI example repo](https://github.com/pipekit/argo-workflows-ci-example) to get a fully local installation of Argo Workflows that will run the two example workflows in this directory. Pull down the repo and add the workflow files over to the directory run them.

You can run the whole installation locally in a k3d cluster. 

## Data processing example - `fan-out-fan-in.yaml`
This example workflow shows how S3 artifact processing can be parallelized with Argo Workflows using a fan-out approach. 

It also includes further artifact configurations:
- `artifactGC` strategy for all artifacts, plus an over-ride for the final output step
- including `{{workflow.uid}}` in the artifact key
- `podSpecPatch` for increased resources for the `reduce` step

## CI example - `ci-workflow-s3.yaml`
This example workflow uses minio as the artifact repository to pass data between steps for a CI workflow that builds and deploys an app to Argo CD. It references WorkflowTemplates located in the [CI example repo](https://github.com/pipekit/argo-workflows-ci-example), so it must be ran as part of that installation.

It also includes further artifact configurations:
- `artifactGC` strategy for all artifacts

## Argo Workflows Support

For more information about Argo Workflows, please see the following resources:


* [The Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)
* [The Argo Workflows GitHub Repository](https://github.com/argoproj/argo-workflows/)
* [The Argo Workflows Slack Channel](https://cloud-native.slack.com/archives/C01QW9QSSSK)

---

## About Pipekit
[Pipekit](pipekit.io) allows you to manage your workflows at scale. The control plane configures Argo Workflows for you in your infrastructure, enabling you to optimize multi-cluster workloads while reducing your cloud spend.  The team at Pipekit is also happy to support you through your Argo Workflows journey via commercial support.
