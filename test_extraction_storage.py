from sqlalchemy import select

from backend.app.core.config import settings
from backend.app.db.session import SessionLocal
from backend.app.models.email import Email
from backend.app.services.ai.extractor import extract_sales_lead
from backend.app.services.ai.extraction_storage import save_sales_lead_extraction


db = SessionLocal()

try:
    email = db.scalar(
        select(Email).order_by(Email.id.desc())
    )

    if email is None:
        print("No emails found.")
        exit()

    extraction = extract_sales_lead(
        sender=email.sender,
        subject=email.subject,
        body=email.body_text,
    )

    record = save_sales_lead_extraction(
        db=db,
        email=email,
        extraction=extraction,
        model=settings.gemini_model,
    )

    print("\n--- SAVED SALES LEAD EXTRACTION ---")

    print("Record ID:", record.id)
    print("Email ID:", record.email_id)
    print("Name:", record.name)
    print("Email:", record.email)
    print("Phone:", record.phone)
    print("Company:", record.company)
    print("Location:", record.location)
    print("Product:", record.product_interest)
    print("Budget:", record.budget)
    print("Timeline:", record.timeline)
    print("Requirements:", record.requirements)
    print("Urgency:", record.urgency)
    print("Model:", record.model)

finally:
    db.close()