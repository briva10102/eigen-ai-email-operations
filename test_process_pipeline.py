from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.email import Email
from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.extraction import SalesLeadExtractionRecord
from backend.app.services.processing.email_processor import process_email


db = SessionLocal()

try:

    email = db.scalar(
        select(Email)
        .where(
            Email.subject == "Solar Installation Quotation Request"
        )
        .order_by(Email.id.desc())
    )

    if email is None:
        print("Quotation email not found.")
        exit()

    print("\n--- PROCESSING EMAIL ---")
    print("Email ID:", email.id)
    print("Subject:", email.subject)

    actions = process_email(
        db=db,
        email_id=email.id,
    )

    classification = db.scalar(
        select(EmailClassificationRecord).where(
            EmailClassificationRecord.email_id == email.id
        )
    )

    extraction = db.scalar(
        select(SalesLeadExtractionRecord).where(
            SalesLeadExtractionRecord.email_id == email.id
        )
    )

    print("\n--- CLASSIFICATION ---")
    print("Category:", classification.category)
    print("Confidence:", classification.confidence)

    print("\n--- EXTRACTION ---")
    print("Name:", extraction.name)
    print("Phone:", extraction.phone)
    print("Location:", extraction.location)
    print("Product:", extraction.product_interest)
    print("Budget:", extraction.budget)
    print("Timeline:", extraction.timeline)

    print("\n--- ACTIONS EXECUTED ---")

    for action in actions:
        print(action)

finally:
    db.close()