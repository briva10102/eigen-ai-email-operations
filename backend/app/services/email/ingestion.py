from sqlalchemy.orm import Session

from backend.app.services.email.gmail import (
    get_gmail_service,
    fetch_message,
)
from backend.app.services.email.normalizer import (
    normalize_gmail_message,
)
from backend.app.services.email.storage import store_email


def ingest_latest_emails(
    db: Session,
    email_account_id: int,
    limit: int = 5,
) -> list:
    service = get_gmail_service()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=limit,
        )
        .execute()
    )

    messages = response.get("messages", [])

    stored_emails = []

    for message in messages:
        raw_message = fetch_message(
            service,
            message["id"],
        )

        normalized_email = normalize_gmail_message(
            raw_message
        )

        email = store_email(
            db=db,
            email_data=normalized_email,
            email_account_id=email_account_id,
        )

        stored_emails.append(email)

    return stored_emails