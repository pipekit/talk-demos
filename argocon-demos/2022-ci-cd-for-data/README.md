# CI/CD for Data Pipelines using Argo Workflows

This demo shows how to run CI on a workflow template. It uses Argo Events to
process Github pull request events and then creates a workflow that does the
following:
1. Updates the `bootstrap/argo-workflows/doubler-template.yaml` WorkflowTemplate
2. Runs the WorkflowTemplate and asserts that the test cases pass

To do so, the sensor relies on the Workflow of Workflows pattern because
WorkflowTemplates used by a Workflow are added at compile time.

Sample text to trigger a PR
