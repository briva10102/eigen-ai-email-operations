from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.email import Email
from backend.app.models.extraction import SalesLeadExtractionRecord
from backend.app.schemas.extraction import SalesLeadExtraction


def save_sales_lead_extraction(
    db: Session,
    email: Email,
    extraction: SalesLeadExtraction,
    model: str,
) -> SalesLeadExtractionRecord:

    existing = db.scalar(
        select(SalesLeadExtractionRecord).where(
            SalesLeadExtractionRecord.email_id == email.id
        )
    )

    if existing:
        return existing

    record = SalesLeadExtractionRecord(
        email_id=email.id,
        name=extraction.name,
        email=extraction.email,
        phone=extraction.phone,
        company=extraction.company,
        location=extraction.location,
        product_interest=extraction.product_interest,
        budget=extraction.budget,
        timeline=extraction.timeline,
        requirements=extraction.requirements,
        urgency=extraction.urgency,
        model=model,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record