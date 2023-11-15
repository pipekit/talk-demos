"""The main fine tuning module that specified what model we want to finetune from Huggingface.

Note that this requires setting an env variable called `HF_TOKEN` with a valid Huggingface authentication token.
This token is used to authenticate with HF and provide the ability to pull the specified model name, in this case
`meta-llama/Llama-2-7b-hf`.

TODO: this script contains all the specifications for finetuning. However, all of these could be parameters
      that are passed in from the command line. This would allow us to run the same script with different parameters
      and finetune different models without rebuilding the container that contains this script.
"""
import os

import huggingface_hub
from llama_recipes.finetuning import main

huggingface_hub.login(os.getenv("HF_TOKEN"))

if __name__ == "__main__":
    main(
        model_name="meta-llama/Llama-2-7b-hf",
        output_dir="/kubecon_na_23_llama2_finetune/finetune/output",
        dist_checkpoint_root_folder="/kubecon_na_23_llama2_finetune/finetune/checkpoint",
        # fsdp=fully sharded data parallel, a technique for training models larger than can fit on a single GPU
        enable_fsdp=True,
        use_fast_kernels=True,
        use_peft=True,
        peft_method="lora",
        # use a batch size of 1 because the GPUs used for the talk only provide ~16Gi of memory
        # and fitting a batch size > 1 can risk OOMs
        batch_size_training=1,
        # for demonstration purposes train for a single epoch. Tested on 1, 2, and 3 epochs
        num_epochs=1,
    )
