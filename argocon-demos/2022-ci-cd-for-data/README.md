# CI/CD for Data Pipelines with Argo Workflows

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io)

## Goal of this repository
- Provide an overview of CI/CD for data pipelines
- Highlight problems solved by CI/CD for data pipelines
- Showcase a development setup of CI/CD for data pipelines using Argo Workflows  

## The talk

[![CI/CD for Data Pipelines with Argo Workflows](https://i3.ytimg.com/vi/729GwVMgeXw/hqdefault.jpg)](https://www.youtube.com/watch?v=729GwVMgeXw)

## Requirements
- Argo Workflows
- Argo Events
- GitHub
- Local K8s environment (k3d, Docker, etc.)

## The demo
This demo shows how to run CI on a workflow template. It uses Argo Events to
process GitHub pull request events and then creates a workflow that does the
following:
1. Updates the `bootstrap/argo-workflows/doubler-template.yaml` WorkflowTemplate
2. Runs the WorkflowTemplate and asserts that the test cases pass

To do so, the sensor relies on the Workflow of Workflows pattern because
WorkflowTemplates used by a Workflow are added at compile time.

## Demo video
[View a recording of this demo on Google Drive here.]()

---

## About Pipekit

[Pipekit](pipekit.io) allows you to manage your workflows at scale. The control plane configures Argo Workflows for you in your infrastructure, enabling you to optimize multi-cluster workloads while reducing your cloud spend.  The team at Pipekit is also happy to support you through your Argo Workflows journey via commercial support.
