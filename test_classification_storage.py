from sqlalchemy import select

from backend.app.core.config import settings
from backend.app.db.session import SessionLocal
from backend.app.models.email import Email
from backend.app.services.ai.classifier import classify_email
from backend.app.services.ai.classification_storage import save_classification


db = SessionLocal()

try:
    email = db.scalar(
        select(Email)
        .order_by(Email.id.desc())
    )

    if email is None:
        print("No emails found.")
        exit()

    classification = classify_email(
        sender=email.sender,
        subject=email.subject,
        body=email.body_text,
    )

    record = save_classification(
        db=db,
        email=email,
        classification=classification,
        model=settings.gemini_model,
    )

    print("\n--- SAVED CLASSIFICATION ---")
    print("Record ID:", record.id)
    print("Email ID:", record.email_id)
    print("Category:", record.category)
    print("Confidence:", record.confidence)
    print("Urgency:", record.urgency)
    print("Intent:", record.intent)
    print("Reason:", record.reason)
    print("Model:", record.model)

finally:
    db.close()