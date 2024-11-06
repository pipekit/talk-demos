"""This module provides functionality for constructing the path to images to be used in workflows.

This module is not limited to providing hardcoded strings for images, such as 'python:3.7'! The module can host very 
customized implementations of how to obtain the image. For example, you can perform logic by invoking 'git' via the
'sh' package, obtain a git SHA for an image, or latest by default, and assemble a path to a Docker image for 
your organization, {{cookiecutter.name}}!
"""


def get_image() -> str:
    """Return the {{cookiecutter.name}} Docker image path to be used in a workflow."""
    sha = 123
    return f"{{cookiecutter.name}}:{sha}" or "{{cookiecutter.name}}:latest"
