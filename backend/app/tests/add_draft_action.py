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

    create_workflow_action_definition(
        db=db,
        workflow_id=workflow.id,
        action_type="GENERATE_DRAFT",
        order=3,
    )

    print("GENERATE_DRAFT added.")

finally:
    db.close()