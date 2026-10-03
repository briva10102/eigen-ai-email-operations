from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.email import Email
from backend.app.models.extraction import SalesLeadExtractionRecord
from backend.app.models.lead import Lead


def create_lead(
    db: Session,
    email: Email,
    extraction: SalesLeadExtractionRecord,
) -> Lead:

    existing_lead = db.scalar(
        select(Lead).where(
            Lead.email_id == email.id
        )
    )

    if existing_lead:
        return existing_lead

    lead = Lead(
        email_id=email.id,
        name=extraction.name,
        email=extraction.email or email.sender,
        phone=extraction.phone,
        company=extraction.company,
        location=extraction.location,
        product_interest=extraction.product_interest,
        budget=extraction.budget,
        timeline=extraction.timeline,
        requirements=extraction.requirements,
        status="NEW",
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return lead