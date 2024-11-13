# Code for Hera Data Science Blog

See the blog markdown in [`assets/hera-data-science.md`](assets/hera-data-science.md).

The files in [ds_blog](ds_blog) demonstrate how to convert a basic Data Science Python script, in
[`diabetes_scenario_script.py`](ds_blog/diabetes_scenario_script.py), into a Hera workflow, by first converting it to a
set of functions, in [`ds_blog/diabetes_functions.py`](ds_blog/diabetes_functions.py), then to a workflow using the
[Script Annotations](https://hera.readthedocs.io/en/stable/user-guides/script-annotations/) feature, in
[`ds_blog/workflow_using_annotated.py`](ds_blog/workflow_using_annotated.py). The
[`ds_blog/workflow_using_pydantic.py`](ds_blog/workflow_using_pydantic.py) file shows some usage of the
[Script Runner IO](https://hera.readthedocs.io/en/stable/user-guides/script-runner-io/) feature, but the feature is not
yet stable/feature complete for a full example.
