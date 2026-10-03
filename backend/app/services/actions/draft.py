from sqlalchemy.orm import Session

from backend.app.models.email import Email
from backend.app.models.email_draft import EmailDraft
from backend.app.models.workflow_run import WorkflowRun
from backend.app.services.ai.draft_generator import generate_email_draft


def create_email_draft(
    db: Session,
    email: Email,
    workflow_run: WorkflowRun,
) -> EmailDraft:

    draft = generate_email_draft(
        sender=email.sender,
        subject=email.subject,
        body=email.body_text,
    )

    email_draft = EmailDraft(
        email_id=email.id,
        workflow_run_id=workflow_run.id,
        subject=draft["subject"],
        body=draft["body"],
        status="PENDING_REVIEW",
    )

    db.add(email_draft)
    db.commit()
    db.refresh(email_draft)

    return email_draft