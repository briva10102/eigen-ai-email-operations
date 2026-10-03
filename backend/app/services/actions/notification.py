from sqlalchemy.orm import Session

from backend.app.models.email import Email
from backend.app.models.notification import Notification
from backend.app.models.workflow_run import WorkflowRun


def create_notification(
    db: Session,
    email: Email,
    workflow_run: WorkflowRun,
    recipient: str,
) -> Notification:

    notification = Notification(
        email_id=email.id,
        workflow_run_id=workflow_run.id,
        recipient=recipient,
        title="New quotation request",
        message=f"New quotation request received from {email.sender}. "
                f"Subject: {email.subject}",
        status="UNREAD",
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification