from sqlalchemy.orm import Session

from backend.app.models.email import Email
from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.extraction import SalesLeadExtractionRecord
from backend.app.models.workflow_run import WorkflowRun

from backend.app.services.actions.lead import create_lead
from backend.app.services.actions.notification import create_notification
from backend.app.services.actions.draft import create_email_draft


def dispatch_action(
    db: Session,
    action_type: str,
    email: Email,
    classification: EmailClassificationRecord,
    extraction: SalesLeadExtractionRecord | None = None,
    workflow_run: WorkflowRun | None = None,
):
    if action_type == "CREATE_LEAD":

        if extraction is None:
            raise ValueError(
                f"Sales lead extraction required for email {email.id}"
            )

        lead = create_lead(
            db=db,
            email=email,
            extraction=extraction,
        )

        return {
            "action": "CREATE_LEAD",
            "success": True,
            "lead_id": lead.id,
        }

    if action_type == "SEND_NOTIFICATION":

        if workflow_run is None:
            raise ValueError(
                "Workflow run required for notification"
            )

        notification = create_notification(
            db=db,
            email=email,
            workflow_run=workflow_run,
            recipient="sales",
        )

        return {
            "action": "SEND_NOTIFICATION",
            "success": True,
            "notification_id": notification.id,
        }

    if action_type == "GENERATE_DRAFT":

        if workflow_run is None:
            raise ValueError(
                "Workflow run required for draft generation"
            )

        draft = create_email_draft(
            db=db,
            email=email,
            workflow_run=workflow_run,
        )

        return {
            "action": "GENERATE_DRAFT",
            "success": True,
            "draft_id": draft.id,
        }

    raise ValueError(
        f"Unsupported action: {action_type}"
    )