from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.workflow import Workflow
from backend.app.services.workflow.action_definition_storage import (
    create_workflow_action_definition,
)


db = SessionLocal()

try:
    workflow = db.scalar(
        select(Workflow)
        .where(Workflow.name == "Quotation Lead Workflow")
    )

    if workflow is None:
        raise ValueError("Quotation Lead Workflow not found")

    existing_actions = db.execute(
        select(
            workflow_action := __import__(
                "backend.app.models.workflow_action_definition",
                fromlist=["WorkflowActionDefinition"],
            ).WorkflowActionDefinition
        ).where(
            workflow_action.workflow_id == workflow.id
        )
    ).scalars().all()

    if not existing_actions:
        create_workflow_action_definition(
            db=db,
            workflow_id=workflow.id,
            action_type="CREATE_LEAD",
            order=1,
        )

        create_workflow_action_definition(
            db=db,
            workflow_id=workflow.id,
            action_type="SEND_NOTIFICATION",
            order=2,
        )

        print("Workflow actions created.")

    else:
        print("Workflow actions already exist.")

finally:
    db.close()