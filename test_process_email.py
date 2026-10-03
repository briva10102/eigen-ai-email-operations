from sqlalchemy import select

from backend.app.core.config import settings
from backend.app.db.session import SessionLocal

from backend.app.models.email import Email
from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.extraction import SalesLeadExtractionRecord

from backend.app.schemas.classification import EmailCategory

from backend.app.services.ai.classifier import classify_email
from backend.app.services.ai.classification_storage import save_classification
from backend.app.services.ai.extractor import extract_sales_lead
from backend.app.services.ai.extraction_storage import save_sales_lead_extraction


db = SessionLocal()

try:
    # Find our original test email
    email = db.scalar(
        select(Email)
        .where(Email.subject == "EIGEN TEST EMAIL")
        .order_by(Email.id.desc())
    )

    if email is None:
        print("EIGEN TEST EMAIL not found.")
        exit()

    print("\n--- EMAIL FOUND ---")
    print("Email ID:", email.id)
    print("Subject:", email.subject)
    print("From:", email.sender)

    # -----------------------------
    # CLASSIFICATION
    # -----------------------------

    classification = classify_email(
        sender=email.sender,
        subject=email.subject,
        body=email.body_text,
    )

    # For this test email, Gemini may classify it as something other
    # than QUOTATION. We need a real business email for the workflow.
    print("\n--- CLASSIFICATION ---")
    print("Category:", classification.category)
    print("Confidence:", classification.confidence)
    print("Intent:", classification.intent)

    classification_record = save_classification(
        db=db,
        email=email,
        classification=classification,
        model=settings.gemini_model,
    )

    print("Classification saved:", classification_record.id)

    # -----------------------------
    # EXTRACTION
    # -----------------------------

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
    print("Phone:", extraction_record.phone)
    print("Location:", extraction_record.location)
    print("Product:", extraction_record.product_interest)

    print("\nProcessing complete.")

finally:
    db.close()