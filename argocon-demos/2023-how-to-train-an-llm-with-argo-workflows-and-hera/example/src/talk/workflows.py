"""The workflows module is a light wrapper around Hera.

This module sets up several interceptors / Hera hooks that intercept workflows prior to creation to add necessary
fields like volumes, default image pull policies, auth, etc. There are several environment variables that must be
set in order for this script to function. Specifically, the following must be set:
- `ARGO_HOST`: the Argo host to use, such as `https://my-api-server.com`
- `ARGO_TOKEN`: the Argo token to use for authentication
- `ARGO_NAMESPACE`: the Argo namespace to use for the workflows
"""
import os

from hera.shared import global_config, register_pre_build_hook
from hera.workflows import *  # noqa
from hera.workflows import (
    Container,
    EmptyDirVolume,
    models as m,  # noqa
)

# TODO: the following are environment variables that must be set in order for the workflows to run!
global_config.host = os.getenv("ARGO_HOST")
global_config.token = os.getenv("ARGO_TOKEN")
global_config.namespace = os.getenv("ARGO_NAMESPACE")
# this image was constructed from the talk `Dockerfile`. It's best to construct your own!
global_config.image = "flaviuvadan/kubecon-na-23-finetune-llama2:latest"


@register_pre_build_hook
def add_image_pull_policy_to_container(c: Container) -> Container:
    """Adds a default image pull policy to the container if one is not already set.

    This always sets the policy to `Always` to ensure that the latest image is used in case the container is rebuilt.
    """
    if c.image_pull_policy is None:
        c.image_pull_policy = "Always"
    return c


@register_pre_build_hook
def add_necessary_tolerations_and_selectors_for_gpus(c: Container) -> Container:
    """Adds necessary tolerations and selectors for GPU nodes."""
    if c.resources is None:
        return c

    if c.resources.gpus is None:
        return c

    if c.resources.gpus > 0:
        t = m.Toleration(
            key="nvidia.com/gpu", operator="Equal", value="present", effect="NoSchedule"
        )
        if c.tolerations is None:
            c.tolerations = [t]
        else:
            c.tolerations += [t]

        selectors = {
            # TODO: set this to whatever cloud provider influenced selector you need to use! The talk was executed
            #       on GCP / GKE, hence the `cloud.google.com` selector for NVIDIA T4s
            "cloud.google.com/gke-accelerator": "nvidia-tesla-t4",
        }
        if c.node_selector is None:
            c.node_selector = selectors
        else:
            c.node_selector |= selectors

    return c


@register_pre_build_hook
def add_empty_dir_shm_vol_to_multi_gpu_tasks(c: Container) -> Container:
    """Adds an empty dir volume to multi-GPU tasks to enable shared memory communication between GPUs.

    If this is not set the training job might fail with an error like: `Python bus error`. This is because the job
    attempts to access the shared memory space of the node for intercommunication, and if Linux catches an invalid
    memory access _without_ /dev/shm mounted, then it will manifest as a bus error.
    """
    if c.resources is None:
        return c

    if c.resources.gpus is None:
        return c

    if c.resources.gpus > 0:
        vol = EmptyDirVolume(name="gpu-comm", size_limit="50Gi", mount_path="/dev/shm")
        vol_mnt = m.VolumeMount(mount_path="/dev/shm", name="gpu-comm")

        if c.volumes is None:
            c.volumes = [vol]
        else:
            c.volumes += [vol]

        # number of volume mounts might be different than the number of volumes, so set this differently
        if c.volume_mounts is None:
            c.volume_mounts = [vol_mnt]
        else:
            c.volume_mounts += [vol_mnt]
    return c
