from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.email import Email
from backend.app.services.workflow.engine import workflow_matches
from backend.app.services.workflow.storage import get_enabled_workflows


db = SessionLocal()

try:
    email = db.scalar(
        select(Email).order_by(Email.id.desc())
    )

    if email is None:
        print("No emails found.")
        exit()

    classification = db.scalar(
        select(EmailClassificationRecord).where(
            EmailClassificationRecord.email_id == email.id
        )
    )

    if classification is None:
        print("No classification found for this email.")
        exit()

    workflows = get_enabled_workflows(db)

    print("\n--- REAL WORKFLOW TEST ---")
    print("Email ID:", email.id)
    print("Subject:", email.subject)
    print("Category:", classification.category)
    print("Confidence:", classification.confidence)

    for workflow in workflows:

        matches = workflow_matches(
            workflow=workflow,
            classification=classification,
        )

        print(
            f"\nWorkflow: {workflow.name}"
        )
        print(
            f"Matches: {matches}"
        )

finally:
    db.close()