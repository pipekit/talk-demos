# Data Science Workflows Made Easy: Python-Powered Argo for Your Organization


[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io?utm_campaign=talk-demos)

## The talk
The talk recording [can be found here](https://youtu.be/hZOcj5uVQOo).

The slide deck for this talk can be found [here](assets/slide-deck.pdf).

## Installing and Running

The code used in the talk can be found in the [example folder](example), which
is adapted from the Pipekit blog post
[How To Get the Most out of Hera for Data Science](https://pipekit.io/blog/how-to-get-the-most-out-of-hera-for-data-science).

1. Ensure [docker-desktop](https://www.docker.com/products/docker-desktop/) is running
1. Run `make install-environment`
1. Port forward the argo service and the minio service
1. Run `make add-data`
1. Run `make run`
1. See the workflow at the localhost web address printed to the console

---

## About Pipekit

Pipekit is the control plane for Argo Workflows. Platform teams use Pipekit to manage data & CI pipelines at scale, while giving developers self-serve access to Argo. Pipekit's unified logging view, Workflow Metrics dashboards, enterprise-grade RBAC and multi-cluster management capabilities lower maintenance costs for platform teams while delivering a superior devex for Argo users. Sign up for a 30-day free trial at [pipekit.io/signup](https://pipekit.io/signup?utm_campaign=talk-demos).

Learn more about Pipekit's professional support for companies already using Argo at [pipekit.io/services](https://pipekit.io/services?utm_campaign=talk-demos).
