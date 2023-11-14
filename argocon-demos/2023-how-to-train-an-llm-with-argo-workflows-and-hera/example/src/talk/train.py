"""The main training module.

This module provides the core workflow scheduling logic that:
1. Spins up the necessary etcd resources for distributed training
2. Created the containers that run the training job using `torchrun`
3. Delete the etcd resources after the training job is done

There are several implicit dependencies in this script:
1. You need a K8s secret called `hf-token` with a field `token` that contains the Huggingface authentication token.
   While not ideal because it's either encoded as plain text or base64 encoded, this is the simplest way to pass the
   token for the talk purposes :) your own infrastructure might have more secure ways to provide this token, such as
   a secret vault that uses a specific service account for authentication/authorization to fetch the token
"""
from random import randint

from talk.etcd import (
    create_etcd_load_balancer,
    create_etcd_stateful_set,
    delete_etcd_resources,
    wait_for_etcd_ip,
)
from talk.ssd import create_ssd_storage_class
from talk.workflows import (
    DAG,
    Container,
    FieldEnv,
    Parameter,
    Resources,
    SecretEnv,
    Workflow,
    m,
)

"""NUM_NODES dictates the number of nodes that training should run on."""
NUM_NODES = 4

"""finetune is the main container that runs part of a training job given node configuration."""
finetune = Container(
    name="fine-tune-rank-n",
    env=[
        SecretEnv(name="HF_TOKEN", secret_name="hf-token", secret_key="token"),
        FieldEnv(name="LOCAL_IP", field_path="status.podIP"),
    ],
    # the following is a public image built for the talk. It only contains the files in this repo along with an update
    # to a torch dev / nightly version so that we can use the latest FSDP features and PEFT
    image="flaviuvadan/kubecon-na-23-finetune-llama2:latest",
    # https://pytorch.org/docs/stable/elastic/run.html
    command=["torchrun"],
    args=[
        # the number of K8s nodes to use for training. For the talk this was tested on 1 node with 4 GPUs and
        # also tested on 4 nodes with 4 GPUs = 16 GPU training
        "--nnodes",
        NUM_NODES,
        # the number of processes per node / number of GPUs
        "--nproc-per-node",
        NUM_NODES,
        # randezvous backend is the mechanism used to coordinate the training job. etcd-v2 is the recommended one for
        # `nnodes` > 1 while c10d is recommended for single node training. Note, the use of the v2 etcd API must be
        # enabled by the etcd resource
        "--rdzv-backend",
        "etcd-v2",
        # the etcd endpoint is the load balancer service that exposes the etcd pods
        "--rdzv-endpoint",
        "{{inputs.parameters.etcd-ip}}:2379",
        # the rdzv id is a unique identifier for the training job. It's used to coordinate the training job
        "--rdzv-id",
        "{{inputs.parameters.rdvz-id}}",
        # the node rank is the rank of the current node in the training job. It's used to coordinate the training job.
        # Rank 0 is the "main" rank that contains the officially finetuned model whereas the other nodes are "worker"
        # nodes / ranks
        "--node-rank",
        "{{inputs.parameters.node-rank}}",
        # the local address is the IP address of the current node
        "--local-addr",
        "$(LOCAL_IP)",
        # the maximum number of worker group restarts before the whole job fails
        "--max-restarts",
        "3",
        # the actual training job path within the container
        "/kubecon_na_23_llama2_finetune/src/talk/finetune.py",
    ],
    inputs=[
        Parameter(name="rdvz-id"),
        Parameter(name="node-rank"),
        Parameter(name="node-vol"),
        Parameter(name="etcd-ip"),
    ],
    # these were identified empirically / by trial + some online documentation about LLM training
    resources=Resources(
        cpu_request=8, cpu_limit=12, memory_request="112Gi", memory_limit="120Gi", gpus=4
    ),
    # here we use a dynamic volume mount because we expect the workflow to spin up a number of volumes equal to the
    # number of nodes we use for training. If this were to use the `volumes` field it would spin up a single volume
    # in `ReadWriteOnce`, preventing the different nodes to mount the same disk. This would work if you have a
    # network volume with `ReadWriteMany` access mode, though!
    volume_mounts=[
        m.VolumeMount(
            mount_path="/kubecon_na_23_llama2_finetune/finetune",
            name="{{inputs.parameters.node-vol}}",
        ),
    ],
)

# the main workflow that schedules:
# 1. etcd resource creation
# 2. Actual training job
# 3. etcd resource deletion
with Workflow(
    generate_name="fine-tune-llm-",
    entrypoint="fine-tune",
    # these volume claim templates are the ones use for dynamically spinning up volumes for the training job, equal
    # to the number of nodes that are created for training
    volume_claim_templates=[
        m.PersistentVolumeClaim(
            metadata=m.ObjectMeta(name=f"rank-{i}"),
            spec=m.PersistentVolumeClaimSpec(
                resources=m.ResourceRequirements(
                    requests={"storage": "20Gi"}, limits={"storage": "20Gi"}
                ),
                # TODO: it's possible to spin up pods in one zone of a region and a disk in another zone of a region!
                #       I recommend setting a `storage_class_name` that specifically tells K8s that it should create
                #       the volumes only when pods actually want to _mount_ a volume! That way the disks are
                #       provisioned in the same zone as the pods are. You will likely need a custom K8s storage class
                #       that uses `volumeBindingMode: WaitForFirstConsumer` :) see `talk.ssd` for more details!
                # storage_class_name="???",
                access_modes=["ReadWriteOnce"],
            ),
        )
        for i in range(0, NUM_NODES)
    ],
) as w:
    # a random ID for the training job. This is used to coordinate the training job and it can be any integer
    rdvz_id = randint(1, 10_000)
    with DAG(name="fine-tune"):
        (
            create_ssd_storage_class()
            >> [
                create_etcd_stateful_set(),
                create_etcd_load_balancer(),
            ]
            >> wait_for_etcd_ip(
                arguments={
                    "service-name": "{{tasks.create-etcd-load-balancer.outputs.parameters.etcd-svc-name}}"
                }
            )
            >> [
                finetune(
                    name=f"finetune-rank-{i}",
                    arguments={
                        "rdvz-id": rdvz_id,
                        "node-rank": i,
                        "node-vol": f"rank-{i}",
                        "etcd-ip": "{{tasks.wait-for-etcd-load-balancer-ip.outputs.parameters.etcd-ip}}",
                    },
                )
                for i in range(0, NUM_NODES)
            ]
        )

    # clean up the created resources
    with DAG(name="exit") as exit_dag:
        delete_etcd_resources()

    w.on_exit = exit_dag

# finally, create the training workflow!!!
w.create()
