"""This is a simple auth module.

This module provides authentication features for submitting workflows. Specifically, it contains small functions
that generate authentication tokens for the organization {{cookiecutter.name}}. Note that the way tokens, 
hosts, etc, are generated is arbitrary and custom to the organization! Bring your own implementation, and it will
work with Hera!
"""


def get_token() -> str:
    """Return an authentication token for {{cookiecutter.name}}'s platform."""
    return "Bearer 123"
