from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.email_account import EmailAccount, EmailProvider
from backend.app.services.email.ingestion import ingest_latest_emails


db = SessionLocal()

try:
    email_account = db.scalar(
        select(EmailAccount).where(
            EmailAccount.email_address == "YOUR_DUMMY_GMAIL@gmail.com"
        )
    )

    if email_account is None:
        email_account = EmailAccount(
            email_address="YOUR_DUMMY_GMAIL@gmail.com",
            provider=EmailProvider.GMAIL,
        )

        db.add(email_account)
        db.commit()
        db.refresh(email_account)

    emails = ingest_latest_emails(
        db=db,
        email_account_id=email_account.id,
        limit=5,
    )

    print(f"Stored/found {len(emails)} emails")

    for email in emails:
        print("\n--- EMAIL ---")
        print("ID:", email.id)
        print("From:", email.sender)
        print("Subject:", email.subject)
        print("Thread ID:", email.thread_id)

finally:
    db.close()