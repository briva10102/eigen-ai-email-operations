from sqlalchemy import select

from backend.app.core.config import settings
from backend.app.db.session import SessionLocal

from backend.app.models.email import Email

from backend.app.services.ai.classifier import classify_email
from backend.app.services.ai.classification_storage import save_classification

from backend.app.services.ai.extractor import extract_sales_lead
from backend.app.services.ai.extraction_storage import save_sales_lead_extraction


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
        print("Solar quotation email not found.")
        exit()

    print("\n--- REAL EMAIL ---")
    print("Email ID:", email.id)
    print("Subject:", email.subject)
    print("From:", email.sender)

    # -------------------------
    # CLASSIFICATION
    # -------------------------

    classification = classify_email(
        sender=email.sender,
        subject=email.subject,
        body=email.body_text,
    )

    classification_record = save_classification(
        db=db,
        email=email,
        classification=classification,
        model=settings.gemini_model,
    )

    print("\n--- CLASSIFICATION ---")
    print("Category:", classification_record.category)
    print("Confidence:", classification_record.confidence)
    print("Urgency:", classification_record.urgency)
    print("Intent:", classification_record.intent)

    # -------------------------
    # EXTRACTION
    # -------------------------

    extraction = extract_sales_lead(
        sender=email.sender,
        subject=email.subject,
        body=email.body_text,
    )

    extraction_record = save_sales_lead_extraction(
        db=db,
        email=email,
        extraction=extraction,
        model=settings.gemini_model,
    )

    print("\n--- EXTRACTION ---")
    print("Name:", extraction_record.name)
    print("Email:", extraction_record.email)
    print("Phone:", extraction_record.phone)
    print("Location:", extraction_record.location)
    print("Product:", extraction_record.product_interest)
    print("Budget:", extraction_record.budget)
    print("Timeline:", extraction_record.timeline)
    print("Requirements:", extraction_record.requirements)

    print("\n--- PROCESSING COMPLETE ---")

finally:
    db.close()