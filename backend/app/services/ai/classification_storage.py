from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.email import Email
from backend.app.schemas.classification import EmailClassification


def save_classification(
    db: Session,
    email: Email,
    classification: EmailClassification,
    model: str,
) -> EmailClassificationRecord:

    existing = db.scalar(
        select(EmailClassificationRecord).where(
            EmailClassificationRecord.email_id == email.id
        )
    )

    if existing:
        return existing

    record = EmailClassificationRecord(
        email_id=email.id,
        category=classification.category,
        confidence=classification.confidence,
        urgency=classification.urgency,
        intent=classification.intent,
        reason=classification.reason,
        model=model,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record