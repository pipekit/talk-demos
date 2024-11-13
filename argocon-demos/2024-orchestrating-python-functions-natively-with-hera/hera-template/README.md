# The Hera demo repository

This repository contains a simple example of an organization's potential internal package that facilitates the 
creation and submission of workflows to Argo via Hera.

The main template is stored in `hera-template`. [Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/) is used
as the main tool to create a demo repository from a template. The `hera-template` contains a `cookiecutter.json` file
that parameterizes the template with the `project_name`, which is the name of the organization the demo is created for.

# Tooling

- Python 3.11
- Poetry 1.4+

# Usage

- Get a working virtual environment using Poetry: `poetry shell`
- Install deps `poetry install`
- Run `cookiecutter hera-template`
    - you will be prompted for a name! Use the organization name which you are preparing a demo for!
