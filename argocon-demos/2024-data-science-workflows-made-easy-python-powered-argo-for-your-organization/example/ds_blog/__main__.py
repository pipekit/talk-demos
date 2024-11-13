from typing import cast
from hera.workflows import Workflow, WorkflowsService
from hera.workflows import models as m


def run_workflow(w: Workflow):
    w.namespace = "argo"
    w.workflows_service = WorkflowsService(
        host="http://localhost:2746",
        verify_ssl=False,
    )
    submitted_w = cast(m.Workflow, w.create())
    print(f"Submitted {submitted_w.metadata.name}")
    print(f"Open http://localhost:2746/workflows/argo/{submitted_w.metadata.name}")


if __name__ == "__main__":
    from ds_blog.a3a_workflow import w

    run_workflow(w)
