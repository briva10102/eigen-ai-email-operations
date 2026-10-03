from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.email import Email


db = SessionLocal()

try:
    emails = db.scalars(
        select(Email).order_by(Email.id)
    ).all()

    print("\n--- EMAILS IN DATABASE ---")

    for email in emails:
        print(
            f"ID: {email.id} | "
            f"Subject: {email.subject} | "
            f"From: {email.sender}"
        )

finally:
    db.close()