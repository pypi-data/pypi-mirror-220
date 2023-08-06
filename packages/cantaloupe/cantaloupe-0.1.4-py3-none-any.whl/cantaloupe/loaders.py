from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

import yaml

from .models import Context, Workflow


def load_workflow(workflow_path: str) -> Workflow:
    """
    Loads a workflow from a given path.

    :param workflow_path: Path to the workflow
    :return: workflow
    """

    if not workflow_path.endswith(".yaml"):
        workflow_path = f"{workflow_path}.yaml"

    with open(workflow_path, "r") as workflow:
        return Workflow(
            **yaml.safe_load(Path(workflow_path).read_text()),
            file_name=workflow.name,
            file_path=workflow_path,
        )


def load_workflows(workflows: Path) -> Iterable[Workflow]:
    """
    Loads all workflows from a given path.

    Note: Workflow files must be named workflow_*.yaml

    :param workflows: Path containing workflows
    :return: iterable of workflows
    """
    for workflow in workflows.glob("*.yaml"):
        if workflow.is_file() and workflow.name.startswith("workflow_"):
            yield Workflow(
                **yaml.safe_load(workflow.read_text()),
                file_name=workflow.name,
                file_path=workflow,
            )


def load_context(workflows: Path) -> Context | None:
    """
    Loads the context file from a given directory.

    :param workflows: directory containing the workflows
    :type workflows: Path
    :return: context file as a dictionary
    :rtype: dict[str, Any] | None
    """

    context_file = Path(os.path.join(workflows, "context.yaml"))
    if context_file.exists():
        return Context(**yaml.safe_load(context_file.read_text()))
    return None
