# Configuring Volumes for Parallel Workflow Reads and Writes

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io?utm_campaign=talk-demos)

The tests used in the Argocon [Lightning Talk: Configuring Volumes for Parallel Workflow Reads and Writes - Lukonde Mwila, Amazon Web Services & Tim Collins, Pipekit
](https://sched.co/1Jo9v)

NFS-server-provisioner     |  S3
:-------------------------:|:-------------------------:
![](assets/nfs-test.png)   |  ![](assets/s3-test.png)

## The talk
The talk [can be found here](https://www.youtube.com/watch?v=QZI-LXJGWYI).

The slide deck for this talk can be found [here](assets/slide-deck.pdf).

## Tests
The tests require:

- A configured Workflow environment with S3 configured as an artifact repository.
- nfs-server-provisioner installed in the cluster, using `nfs` as the storage class name.
  - The test requires a minimum of 40Gi of storage (either ephemeral or mounted from a persistent volume)

Tests are found in in the [tests](tests) directory of this repo.

## Workflow configuration
The workflow controller configmap configuration we used is in the [workflows-config](workflows-config) directory of this repo. However, more information on setting up an S3 artifact repository with Argo Workflows can be found in the [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/configure-artifact-repository/#configuring-aws-s3)

# Further information:

## Working example using nfs-server-provisioner
[Deploys nfs-server-provisioner using Argo CD and uses it in a simple CI workflow](https://github.com/pipekit/argo-workflows-ci-example).

You can run the whole thing locally in a k3d cluster.

This same example also offers the exact same workflow using minio as the artifact repository to pass data between steps. This allows you to compare the setup differences between the two and to decide the best approach for your own use cases.

## NFS-Server-Provisioner
[The repo for the nfs-server provisioner](https://github.com/kubernetes-sigs/nfs-ganesha-server-and-external-provisioner).


---

## About Pipekit

Pipekit is the control plane for Argo Workflows. Platform teams use Pipekit to manage data & CI pipelines at scale, while giving developers self-serve access to Argo. Pipekit's unified logging view, enterprise-grade RBAC, and multi-cluster management capabilities lower maintenance costs for platform teams while delivering a superior devex for Argo users. Sign up for a 30-day free trial at [pipekit.io/signup](https://pipekit.io/signup?utm_campaign=talk-demos).

Learn more about Pipekit's professional support for companies already using Argo at [pipekit.io/services](https://pipekit.io/services?utm_campaign=talk-demos).
