from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.email_draft import EmailDraft
from backend.app.models.email import Email
from backend.app.services.actions.send_email import send_approved_email


def approve_draft(db, draft_id, reviewer):
    draft = db.scalar(
        select(EmailDraft).where(EmailDraft.id == draft_id)
    )

    if draft is None:
        raise ValueError("Draft not found")

    if draft.status != "PENDING_REVIEW":
        raise ValueError("Draft is not pending review")

    email = db.scalar(
        select(Email).where(Email.id == draft.email_id)
    )

    if email is None:
        raise ValueError("Original email not found")

    draft.status = "APPROVED"
    draft.reviewed_by = reviewer
    draft.reviewed_at = datetime.now(timezone.utc)

    db.commit()

    try:
        result = send_approved_email(
            email=email,
            draft=draft,
        )

        draft.status = "SENT"
        draft.sent_at = datetime.now(timezone.utc)
        draft.provider_message_id = result["provider_message_id"]

        db.commit()
        db.refresh(draft)

        return draft

    except Exception as error:
        draft.status = "SEND_FAILED"
        db.commit()
        raise ValueError(f"Failed to send email: {error}")


def update_draft(
    db: Session,
    draft_id: int,
    subject: str,
    body: str,
) -> EmailDraft:

    draft = db.scalar(
        select(EmailDraft)
        .where(EmailDraft.id == draft_id)
    )

    if draft is None:
        raise ValueError(
            f"Draft {draft_id} not found"
        )

    if draft.status != "PENDING_REVIEW":
        raise ValueError(
            f"Draft {draft_id} is already {draft.status}"
        )

    draft.subject = subject
    draft.body = body

    db.commit()
    db.refresh(draft)

    return draft

def reject_draft(
    db: Session,
    draft_id: int,
    reviewer: str,
) -> EmailDraft:

    draft = db.scalar(
        select(EmailDraft)
        .where(EmailDraft.id == draft_id)
    )

    if draft is None:
        raise ValueError(
            f"Draft {draft_id} not found"
        )

    if draft.status != "PENDING_REVIEW":
        raise ValueError(
            f"Draft {draft_id} is already {draft.status}"
        )

    draft.status = "REJECTED"
    draft.reviewed_by = reviewer
    draft.reviewed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(draft)

    return draft