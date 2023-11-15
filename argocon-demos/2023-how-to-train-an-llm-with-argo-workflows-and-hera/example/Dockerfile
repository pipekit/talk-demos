# The main Dockerfile for the talk! This extends the official PyTorch CUDA 11.8 image
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# set a default working directory for the container
WORKDIR /kubecon_na_23_llama2_finetune

# upgrade dependencies and install poetry as this project relies on poetry
RUN pip3 install --upgrade pip setuptools wheel poetry

# copy over the pyproject + lock file and install the dependencies
COPY pyproject.toml poetry.lock README.md /kubecon_na_23_llama2_finetune/

# install deps globally because this is an experimental container
RUN poetry config virtualenvs.create false

# only install the main project dependencies without the project itself / no root. This way we help Docker cache the
# Python dependencies and only rebuild the container when the dependencies change rather than on every code change
RUN poetry install --all-extras --no-root --only main

# copy over the source code now
COPY src /kubecon_na_23_llama2_finetune/src

# install the project itself! The dependencies are already installed, as mentioned above
RUN poetry install --no-interaction --only-root -v
RUN mkdir /kubecon_na_23_llama2_finetune/finetune

# install the nightly PyTorch build for CUDA 11.8. Note that this is required for FSDP + PEFT, as documented by Meta's
# llama-recipes repository
RUN pip3 install --upgrade --pre torch==2.1.0.dev20230816+cu118 --index-url https://download.pytorch.org/whl/nightly/cu118

# env variables for CUDA and NCCL
ENV LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64 \
    CUDA_LAUNCH_BLOCKING=0 \
    PYTHONFAULTHANDLER=1 \
    NCCL_DEBUG_SUBSYS=WARN \
    NCCL_DEBUG=WARN \
    LOGLEVEL=INFO

