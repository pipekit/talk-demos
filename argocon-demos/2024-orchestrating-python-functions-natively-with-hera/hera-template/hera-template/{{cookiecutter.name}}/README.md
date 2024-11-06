# {{cookiecutter.name}} Hera package template!

This is a template for creating a Hera package for {{cookiecutter.name}}. This package is intended to help your
organization in its adoption journey of Hera and Argo Workflows! The package is named after your organization. The
package consists of several modules. Specifically, the modules are sample modules that allow your organization to
create elements such as paths to Dockerfiles that should be used by Argo workflows, how to authenticate against your
own Argo Server (or a hosted one!), and sets up several example defaults in the workflows module.

# Toolchain

For demonstration purposes there are several tools that are used:

- Python 3.11
- Poetry for package management
- Hera as the default Python SDK to support interactions with Argo Workflows!

# Getting started

- Install Python 3.11
- Install Poetry
- In this repository/folder, run `poetry install`
    - This installs all the necessary dependencies
- Run `poetry shell`
    - This activates a virtual environment that will allow you to play with the package!

# Using the package

Once you have your virtual environment we can simple "Hello, world!" workflow!

```python
# this imports everything we need from the {{cookiecutter.name}} workflows module. This import will make
# the module perform all the necessary setup work for us to use Argo!
from {{cookiecutter.name}}.workflows import Workflow, script, DAG


# this magic decorator actually defines a template for Argo! Hera will take this function upon its invocation and
# turn it into a template that Argo can use! Note that this decorator does not limit your function to remote 
# executions only. You can still use it as a normal Python function outside of a workflow/dag/steps context!
@script()
def hello(name: str):
    print("Hello, {name}!".format(name=name))


# The workflow needs not only a name, but an entrypoint. This is because the workflow can contain many, many elements!
# There can be many templates, many invocations of the said templates via tasks, steps, etc. The entrypoint is the 
# feature that allows us to tell Argo which template to run first!
with Workflow(name="{{cookiecutter.name}}-testing-argo", entrypoint="dag") as w:
    # here, we define the very first template that Argo will run. This template is a DAG, which is a directed acyclic
    # graph that will contain 2 tasks
    with DAG(name="dag"):
        # while we can invoke `hello` as a simple function, it actually gets automatically turned into a `Task` here!
        # Therefore, we have to name it in order to maintain naming uniqueness in Argo!
        hello(name="hello1", arguments={"name": "{{cookiecutter.name}}"})
        hello(name="hello2", arguments={"name": "world"})

# finally, let's create the workflow!
w.create()
```
