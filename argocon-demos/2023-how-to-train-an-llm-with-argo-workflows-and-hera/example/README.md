# KubeCon NA 2023 - How to fine tune an LLM with Argo Workflows and Hera

## Introduction

This repository contains the code and instructions to reproduce the demo presented in the talk titled
"How to fine tune an LLM with Argo Workflows and Hera" KubeCon NA 2023, by Flaviu Vadan and JP Zivalich.

## Talk

- https://colocatedeventsna2023.sched.com/event/1Rj3z/how-to-train-an-llm-with-argo-workflows-and-hera-jp-zivalich-pipekit-flaviu-vadan-dyno-therapeutics
- TODO: add YouTube link

## Prerequisites

- Python 3.10.13
- Poetry 1.6.1
- Docker 20+

## Installation

1. Clone the repository
1. Install the dependencies with `poetry shell && poetry install`
1. Set up the following environment variables:
    1. `ARGO_HOST` - host of your Argo Workflows server
    1. `ARGO_TOKEN` - token to authenticate with the Argo Workflows server
    1. `ARGO_NAMESPACE` - namespace to submit finetuning workflow to
    1. `HF_TOKEN` - HuggingFace authentication token
1. Run `python src/talk/finetune.py` to submit the core finetuning workflow

## Structure

```
├── src
│   ├── talk
│       ├── etcd  # provides resources to create, wait for, and delete the etcd load balancer and replica set
│       ├── finetune  # provides the main Python command for finetuning Llama2 using llama-recipes 
│       ├── ssd  # provides the storage class definition for SSD storage, which is used by etcd 
│       ├── train  # provides the core training workflow that sets up the training containers via Torch, etcd, etc.
│       ├── workflows  # light wrapper around Hera to add labels, set up auth, add GPU tolerations automatically, etc. 
```

## License

This repository observes, follows, and presents the Llama 2 community license agreement (the "license"), Llama 2
Version Release Date: July 18, 2023. Any use of this repository is subject to the terms and conditions of the license.


