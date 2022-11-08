# CI/CD for Data Pipelines using Argo Workflows

## Goal of this repository
- Showcase how Spark Jobs can be orchestrated with Argo Workflows
- Provide a how-to steps to run all examples on local.  

## The talk

[![Processing petabytes in Python with Argo Workflows & Dask](https://img.youtube.com/vi/f5lPS9WKy_8/0.jpg)](https://www.youtube.com/watch?v=f5lPS9WKy_8)

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
