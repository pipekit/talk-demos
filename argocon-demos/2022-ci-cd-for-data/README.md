# CI/CD for Data Pipelines with Argo Workflows

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
