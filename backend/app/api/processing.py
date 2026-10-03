from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from backend.app.services.processing.email_processor import process_email
from backend.app.db.session import SessionLocal
from backend.app.models.email import Email
from backend.app.services.processing.email_processor import process_email


router = APIRouter(
    prefix="/emails",
    tags=["Email Processing"],
)


@router.post("/{email_id}/process")
def process_email_endpoint(email_id: int):
    db = SessionLocal()

    try:
        email = db.scalar(
            select(Email).where(Email.id == email_id)
        )

        if email is None:
            raise HTTPException(
                status_code=404,
                detail="Email not found",
            )

        try:
            actions = process_email(
                db=db,
                email_id=email_id,
            )

            return {
                "email_id": email_id,
                "success": True,
                "actions": actions,
            }

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=str(error),
            )

    finally:
        db.close()