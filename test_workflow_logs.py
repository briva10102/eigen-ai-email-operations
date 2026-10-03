from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.workflow_run import WorkflowRun
from backend.app.models.workflow_action import WorkflowAction


db = SessionLocal()

try:

    runs = db.scalars(
        select(WorkflowRun)
        .order_by(WorkflowRun.id.desc())
    ).all()

    print("\n--- WORKFLOW RUNS ---")

    for run in runs:
        print(
            f"Run ID: {run.id} | "
            f"Workflow ID: {run.workflow_id} | "
            f"Email ID: {run.email_id} | "
            f"Status: {run.status}"
        )

    actions = db.scalars(
        select(WorkflowAction)
        .order_by(WorkflowAction.id.desc())
    ).all()

    print("\n--- WORKFLOW ACTIONS ---")

    for action in actions:
        print(
            f"Action ID: {action.id} | "
            f"Run ID: {action.workflow_run_id} | "
            f"Type: {action.action_type} | "
            f"Status: {action.status} | "
            f"Result: {action.result}"
        )

finally:
    db.close()