from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.workflow_action_definition import WorkflowActionDefinition


def create_workflow_action_definition(
    db: Session,
    workflow_id: int,
    action_type: str,
    order: int,
) -> WorkflowActionDefinition:

    action = WorkflowActionDefinition(
        workflow_id=workflow_id,
        action_type=action_type,
        enabled=True,
        order=order,
    )

    db.add(action)
    db.commit()
    db.refresh(action)

    return action


def get_workflow_actions(
    db: Session,
    workflow_id: int,
) -> list[WorkflowActionDefinition]:

    return list(
        db.scalars(
            select(WorkflowActionDefinition)
            .where(
                WorkflowActionDefinition.workflow_id == workflow_id,
                WorkflowActionDefinition.enabled.is_(True),
            )
            .order_by(WorkflowActionDefinition.order)
        ).all()
    )