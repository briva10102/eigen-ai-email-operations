from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.email import Email
from backend.app.models.workflow import Workflow
from backend.app.schemas.classification import EmailCategory
from backend.app.services.workflow.executor import execute_workflow


db = SessionLocal()

try:
    classification = db.scalar(
        select(EmailClassificationRecord)
        .where(
            EmailClassificationRecord.category == EmailCategory.QUOTATION
        )
        .order_by(EmailClassificationRecord.id.desc())
    )

    if classification is None:
        print("No QUOTATION classification found.")
        exit()

    email = db.scalar(
        select(Email).where(
            Email.id == classification.email_id
        )
    )

    if email is None:
        print("Email for classification not found.")
        exit()

    workflow = db.scalar(
        select(Workflow)
        .where(
            Workflow.enabled.is_(True),
            Workflow.trigger_category == "QUOTATION",
        )
    )

    if workflow is None:
        print("No enabled QUOTATION workflow found.")
        exit()

    print("\n--- REAL WORKFLOW EXECUTION ---")
    print("Email:", email.subject)
    print("Category:", classification.category)
    print("Confidence:", classification.confidence)
    print("Workflow:", workflow.name)

    actions = execute_workflow(
        db=db,
        workflow=workflow,
        email=email,
        classification=classification,
    )

    print("Actions executed:", actions)

finally:
    db.close()