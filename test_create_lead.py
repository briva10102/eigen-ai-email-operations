from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.email import Email
from backend.app.models.extraction import SalesLeadExtractionRecord
from backend.app.services.actions.lead import create_lead


db = SessionLocal()

try:
    email = db.scalar(
        select(Email).order_by(Email.id.desc())
    )

    if email is None:
        print("No emails found.")
        exit()

    extraction = db.scalar(
        select(SalesLeadExtractionRecord).where(
            SalesLeadExtractionRecord.email_id == email.id
        )
    )

    if extraction is None:
        print("No sales lead extraction found.")
        exit()

    lead = create_lead(
        db=db,
        email=email,
        extraction=extraction,
    )

    print("\n--- LEAD CREATED ---")
    print("Lead ID:", lead.id)
    print("Email ID:", lead.email_id)
    print("Name:", lead.name)
    print("Email:", lead.email)
    print("Phone:", lead.phone)
    print("Company:", lead.company)
    print("Location:", lead.location)
    print("Product:", lead.product_interest)
    print("Budget:", lead.budget)
    print("Timeline:", lead.timeline)
    print("Status:", lead.status)

finally:
    db.close()