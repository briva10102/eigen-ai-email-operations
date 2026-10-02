from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.email import Email
from backend.app.models.email_account import EmailAccount
from backend.app.models.email_thread import EmailThread


def store_email(
    db: Session,
    email_data: dict,
    email_account_id: int,
) -> Email:
    existing_email = db.scalar(
        select(Email).where(
            Email.provider_message_id
            == email_data["provider_message_id"]
        )
    )

    if existing_email:
        return existing_email

    thread = db.scalar(
        select(EmailThread).where(
            EmailThread.provider_thread_id
            == email_data["provider_thread_id"]
        )
    )

    if thread is None:
        thread = EmailThread(
            provider_thread_id=email_data["provider_thread_id"],
            subject=email_data["subject"],
        )

        db.add(thread)
        db.flush()

    email = Email(
        provider_message_id=email_data["provider_message_id"],
        subject=email_data["subject"],
        sender=email_data["sender_email"],
        recipients=email_data["recipients"],
        body_text=email_data["body"],
        received_at=email_data["received_at"],
        email_account_id=email_account_id,
        thread_id=thread.id,
    )

    db.add(email)
    db.commit()
    db.refresh(email)

    return email