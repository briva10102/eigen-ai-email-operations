from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.config import settings

from backend.app.models.email import Email
from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.extraction import SalesLeadExtractionRecord
from backend.app.models.workflow import Workflow

from backend.app.services.ai.classifier import classify_email
from backend.app.services.ai.classification_storage import save_classification
from backend.app.services.ai.extractor import extract_sales_lead
from backend.app.services.ai.extraction_storage import save_sales_lead_extraction
from backend.app.services.workflow.executor import execute_workflow


def process_email(
    db: Session,
    email_id: int,
) -> list[dict]:

    # -----------------------------
    # 1. Get email
    # -----------------------------

    email = db.scalar(
        select(Email).where(
            Email.id == email_id
        )
    )

    if email is None:
        raise ValueError(
            f"Email {email_id} not found"
        )

    # -----------------------------
    # 2. Classification
    # -----------------------------

    classification = db.scalar(
        select(EmailClassificationRecord).where(
            EmailClassificationRecord.email_id == email.id
        )
    )

    if classification is None:

        result = classify_email(
            sender=email.sender,
            subject=email.subject,
            body=email.body_text,
        )

        classification = save_classification(
            db=db,
            email=email,
            classification=result,
            model=settings.gemini_model,
        )

    # -----------------------------
    # 3. Extraction
    # -----------------------------

    extraction = db.scalar(
        select(SalesLeadExtractionRecord).where(
            SalesLeadExtractionRecord.email_id == email.id
        )
    )

    if extraction is None:

        result = extract_sales_lead(
            sender=email.sender,
            subject=email.subject,
            body=email.body_text,
        )

        extraction = save_sales_lead_extraction(
            db=db,
            email=email,
            extraction=result,
            model=settings.gemini_model,
        )

    # -----------------------------
    # 4. Find workflows
    # -----------------------------

    workflows = db.scalars(
        select(Workflow).where(
            Workflow.enabled.is_(True)
        )
    ).all()

    all_actions = []

    # -----------------------------
    # 5. Execute matching workflows
    # -----------------------------

    for workflow in workflows:

        actions = execute_workflow(
            db=db,
            workflow=workflow,
            email=email,
            classification=classification,
            extraction=extraction,
        )

        all_actions.extend(actions)

    return all_actions