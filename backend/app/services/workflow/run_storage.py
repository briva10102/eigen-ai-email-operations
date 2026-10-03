from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.app.models.workflow_run import WorkflowRun


def start_workflow_run(
    db: Session,
    workflow_id: int,
    email_id: int,
) -> WorkflowRun:

    run = WorkflowRun(
        workflow_id=workflow_id,
        email_id=email_id,
        status="RUNNING",
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    return run


def complete_workflow_run(
    db: Session,
    run: WorkflowRun,
) -> WorkflowRun:

    run.status = "SUCCESS"
    run.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(run)

    return run


def fail_workflow_run(
    db: Session,
    run: WorkflowRun,
    error: str,
) -> WorkflowRun:

    run.status = "FAILED"
    run.error = error
    run.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(run)

    return run