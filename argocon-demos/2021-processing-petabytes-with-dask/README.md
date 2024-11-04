# Processing petabytes in Python with Argo Workflows & Dask

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io?utm_campaign=talk-demos)

## Goal of this repository

* Showcase the combination of Dask and Argo Workflows to dynamically scale a computational workload
* Provide a basic Argo-workflows installation applicable to production-grade kubernetes clusters
    - The set-up has been tested on AWS EKS, and would likely work for similar kubernetes providers
    - The set-up _might_ work for a local kubernetes installation, such as that with docker desktop or k3s (tested on an M3 Pro Mac with 18GB RAM)
* Package a Dask data pipeline into a docker container
* Create an argo workflows WorkflowTemplate and related resources required to scale out the Dask pipeline in kubernetes

## The talk

[![Processing petabytes in Python with Argo Workflows & Dask](https://img.youtube.com/vi/f5lPS9WKy_8/0.jpg)](https://www.youtube.com/watch?v=f5lPS9WKy_8)

## The pipeline

This project includes a Dask data pipeline which showcases a simple set-up of the [Futures Interface](https://docs.dask.org/en/stable/futures.html). The pipeline will:
* Connect to a pre-existing Dask Scheduler
* Consider a set of timeseries weather data for major cities in Spain
* Submit a data-processing task to the available Dask Workers which accepts a single time stamp argument, and returns the name of a city
    - Takes the input timestamp, and extracts windspeed data at this timestamp for each city
    - Identifies the city with the highest windspeed
    - Returns that city's name
* Counts the observations where each city had the fastest windspeed
* Reports the city which is most often the windiest


## Installing and Running on Local Docker Desktop

With `kubectl` installed and Docker Desktop running with Kubernetes enabled:

1. Run `make install`
2. Go to `http://localhost:2746/workflow-templates/customer/windy-city`
3. Click `Submit`

---

## About Pipekit

Pipekit is the control plane for Argo Workflows. Platform teams use Pipekit to manage data & CI pipelines at scale, while giving developers self-serve access to Argo. Pipekit's unified logging view, enterprise-grade RBAC, and multi-cluster management capabilities lower maintenance costs for platform teams while delivering a superior devex for Argo users. Sign up for a 30-day free trial at [pipekit.io/signup](https://pipekit.io/signup?utm_campaign=talk-demos).

Learn more about Pipekit's professional support for companies already using Argo at [pipekit.io/services](https://pipekit.io/services?utm_campaign=talk-demos).
