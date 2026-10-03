from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.workflow import Workflow


def get_enabled_workflows(db: Session) -> list[Workflow]:
    return list(
        db.scalars(
            select(Workflow).where(
                Workflow.enabled.is_(True)
            )
        ).all()
    )


def create_workflow(
    db: Session,
    name: str,
    description: str,
    trigger_category: str,
    min_confidence: float,
) -> Workflow:

    workflow = Workflow(
        name=name,
        description=description,
        enabled=True,
        trigger_category=trigger_category,
        min_confidence=min_confidence,
    )

    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    return workflow