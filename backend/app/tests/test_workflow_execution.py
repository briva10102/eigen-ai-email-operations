from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.email import Email
from backend.app.services.processing.email_processor import process_email


db = SessionLocal()

try:
    email = db.scalar(
        select(Email)
        .where(
            Email.subject == "Solar Installation Quotation Request"
        )
    )

    if email is None:
        raise ValueError("Quotation email not found")

    print(f"Processing email ID: {email.id}")

    actions = process_email(
        db=db,
        email_id=email.id,
    )

    print("\n--- ACTIONS ---")

    for action in actions:
        print(action)

finally:
    db.close()