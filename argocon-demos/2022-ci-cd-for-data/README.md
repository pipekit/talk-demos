# CI/CD for Data Pipelines with Argo Workflows

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io?utm_campaign=talk-demos)

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

---

## About Pipekit

Pipekit is the control plane for Argo Workflows. Platform teams use Pipekit to manage data & CI pipelines at scale, while giving developers self-serve access to Argo. Pipekit's unified logging view, enterprise-grade RBAC, and multi-cluster management capabilities lower maintenance costs for platform teams while delivering a superior devex for Argo users. Sign up for a 30-day free trial at [pipekit.io/signup](https://pipekit.io/signup?utm_campaign=talk-demos).

Learn more about Pipekit's professional support for companies already using Argo at [pipekit.io/services](https://pipekit.io/services?utm_campaign=talk-demos).
