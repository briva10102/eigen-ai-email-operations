from sqlalchemy.orm import Session

from backend.app.models.workflow_action import WorkflowAction


def save_workflow_action(
    db: Session,
    workflow_run_id: int,
    action_type: str,
    status: str,
    result: str | None = None,
    error: str | None = None,
) -> WorkflowAction:

    action = WorkflowAction(
        workflow_run_id=workflow_run_id,
        action_type=action_type,
        status=status,
        result=result,
        error=error,
    )

    db.add(action)
    db.commit()
    db.refresh(action)

    return action