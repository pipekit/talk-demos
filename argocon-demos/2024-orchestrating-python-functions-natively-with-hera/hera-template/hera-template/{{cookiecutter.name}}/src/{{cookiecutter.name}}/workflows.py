"""This is a simple workflows module that lightly wraps Hera.

This module is dedicated to setting all the necessary defaults for users of workflows at {{cookiecutter.name}}!
All of the settings here provide functionality such as images, defaults for metrics, all the necessary imports from
Hera, global configs such as authentication tokens, hooks for injecting labels, etc.
"""

from hera.shared import *  # noqa

# note that we also import * from Hera. This allows us to expose Hera through our own, thin 
# {{cookiecutter.name}} wrapper, that configures Hera to function as _we_ want to
from hera.workflows import *  # noqa
from hera.workflows import models, models as m  # noqa

from {{cookiecutter.name}}.auth import get_token
from {{cookiecutter.name}}.image import get_image

# Hera allows us to set a server, this assumes that the Argo server is hosted on 
# `argo.{{cookiecutter.name}}.com`
global_config.host = "https://argo.{{cookiecutter.name}}.com"

# Hera allows us to set an image generation function, which returns a `str` that's the Docker image path
global_config.image = get_image

# and we can also set a token on the global config, which allows Hera to generate a token for authentication!
global_config.token = get_token


@register_pre_build_hook
def add_env_to_script(s: Script) -> Script:
    """Add the env variable called `VAR` to a script"""
    var = Env(name="VAR", value="somethig_important_for_{{cookiecutter.name}}")
    if s.env is None:
        s.env = [var]
    else:
        s.env.append(var)
    return s


@register_pre_build_hook
def add_exit_to_workflow(w: Workflow) -> Workflow:
    """Adds an exit script to a workflow if not is not set already."""
    # note that this uses `m` from Hera, which is the models module. That module contains all sorts of 
    # auto-generated objects, such as `Template`! This is the canonical Argo template. So, here, we set an exit
    # template that contains a single container that only prints `Bye` using Python on all workflows that do not
    # have an exit handler! Note that we are not limited to containers, of course. These can be extremely complex 
    # workflows/DAGs/Steps, etc.
    exit_template = m.Template(
        name="exit",
        container=m.Container(
            image="python:3.6",
            command=["python"],
            args=["-c", "print('Bye!')"],
        )
    )
    w.templates.append(exit_template)

    if w.on_exit is None:
        w.on_exit = exit_template.name
    return w


@register_pre_build_hook
def add_image_pull_secrets(w: Workflow) -> Workflow:
    """Add an image pull secret to a workflow so users don't have to configure this on their own."""
    if w.image_pull_secrets is None:
        w.image_pull_secrets = [m.LocalObjectReference(name="{{cookiecutter.name}}-secret")]
    else:
        w.image_pull_secrets.append(m.LocalObjectReference(name="{{cookiecutter.name}}-secret"))
    return w

# there are all sorts of hooks, experimental features, etc, that you can set for Hera, of course! All of these 
# hooks are dedicated towards making your life simpler for setting up your own internal Argo Workflows platform.
# Please consult https://hera.rtfd.io/ for more information! Note that Hera has 1:1 feature parity with Argo Workflows.
# Hence, anything you see on https://argoproj.github.io/workflows can be expressed in Hera!

