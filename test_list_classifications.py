from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.email import Email


db = SessionLocal()

try:
    classifications = db.scalars(
        select(EmailClassificationRecord)
        .order_by(EmailClassificationRecord.id)
    ).all()

    if not classifications:
        print("No classifications found in database.")
        exit()

    print("\n--- CLASSIFICATIONS ---")

    for classification in classifications:
        email = db.scalar(
            select(Email).where(
                Email.id == classification.email_id
            )
        )

        print("\nEmail ID:", classification.email_id)
        print("Subject:", email.subject if email else "Unknown")
        print("Category:", classification.category)
        print("Confidence:", classification.confidence)

finally:
    db.close()