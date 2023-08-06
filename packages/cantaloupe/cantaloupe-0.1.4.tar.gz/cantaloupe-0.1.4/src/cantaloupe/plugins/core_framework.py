import os
import typing
from itertools import chain

from jinja2 import Template

from .. import hookimpl
from ..enums import Action
from ..errors import ValidationError
from ..loaders import load_workflow

if typing.TYPE_CHECKING:
    from ..models import Step, Config, Context, Workflow


@hookimpl
def cantaloupe_resolve_step_variables(step: "Step") -> "Step":
    for key, value in step.variables.items():
        if value.startswith("env:"):
            step.variables[key] = os.getenv(value[4:])
        else:
            step.variables[key] = value

    for key, value in step.config.items():
        if "{{" in value and "}}" in value:
            step.config[key] = Template(value).render(
                {"variables": step.variables}
            )
        else:
            step.config[key] = value

    return step


@hookimpl
def cantaloupe_validate_step_imports(
    index: int,
    step: "Step",
    workflow: "Workflow",
) -> None:
    """
    Validates an import step.
    """
    if step.action == Action.IMPORT and step.use is None:
        msg = (
            f"Step {index} in workflow '{workflow.name}' does not have a 'use' key. "
            "Please provide a workflow to import."
        )
        raise ValidationError(msg)


@hookimpl(tryfirst=True)
def cantaloupe_setup(config: "Config", context: "Context") -> None:
    """
    Called before the build process starts.
    """
    pm = config.pluginmanager

    for workflow in context.workflows:
        steps: list["Step"] = []

        for index, step in enumerate(workflow.steps, start=1):
            pm.hook.cantaloupe_validate_step_imports(
                index=index,
                step=step,
                workflow=workflow,
            )
            if not step.use:
                steps.append(step)
            else:
                # Load the workflow referenced in "use" and merge its steps into the current workflow.
                imported_workflow = load_workflow(
                    os.path.join(config.option.workflows, step.use)
                )
                if not imported_workflow.variables:
                    for imported_steps in imported_workflow.steps:
                        steps.append(imported_steps)
                else:
                    for var in imported_workflow.variables:
                        if var.required and var.name not in step.variables:
                            raise ValidationError(
                                f"Variable {var} is required by the workflow {step.use} but not set."
                            )

                        # use the default value if it exists
                        if (
                            var.name not in step.variables
                            or var.name in step.variables
                            and not step.variables[var.name]
                        ):
                            if var.default:
                                step.variables[var.name] = var.default
                            else:
                                step.variables[var.name] = ""

                    for wf_step in imported_workflow.steps:
                        wf_step.variables = step.variables
                        steps.append(wf_step)

        workflow.steps = list(
            chain(
                *[
                    pm.hook.cantaloupe_resolve_step_variables(
                        workflow=workflow,
                        step=step,
                    )
                    for step in steps
                ]
            )
        )
