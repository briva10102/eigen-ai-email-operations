from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.email_draft import EmailDraft
from backend.app.services.review.draft_review import (
    approve_draft,
    reject_draft,
    update_draft,
)


router = APIRouter(
    prefix="/drafts",
    tags=["Draft Review"],
)


class ReviewRequest(BaseModel):
    reviewer: str


class DraftUpdateRequest(BaseModel):
    subject: str
    body: str


@router.get("")
def get_drafts():

    db = SessionLocal()

    try:
        drafts = db.scalars(
            select(EmailDraft)
            .order_by(EmailDraft.id.desc())
        ).all()

        return drafts

    finally:
        db.close()


@router.get("/{draft_id}")
def get_draft(draft_id: int):

    db = SessionLocal()

    try:
        draft = db.scalar(
            select(EmailDraft)
            .where(EmailDraft.id == draft_id)
        )

        if draft is None:
            raise HTTPException(
                status_code=404,
                detail="Draft not found",
            )

        return draft

    finally:
        db.close()


@router.put("/{draft_id}")
def update_draft_endpoint(
    draft_id: int,
    request: DraftUpdateRequest,
):

    db = SessionLocal()

    try:
        try:
            draft = update_draft(
                db=db,
                draft_id=draft_id,
                subject=request.subject,
                body=request.body,
            )

            return draft

        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )

    finally:
        db.close()


@router.post("/{draft_id}/approve")
def approve_draft_endpoint(
    draft_id: int,
    request: ReviewRequest,
):

    db = SessionLocal()

    try:
        try:
            draft = approve_draft(
                db=db,
                draft_id=draft_id,
                reviewer=request.reviewer,
            )

            return draft

        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )

    finally:
        db.close()


@router.post("/{draft_id}/reject")
def reject_draft_endpoint(
    draft_id: int,
    request: ReviewRequest,
):

    db = SessionLocal()

    try:
        try:
            draft = reject_draft(
                db=db,
                draft_id=draft_id,
                reviewer=request.reviewer,
            )

            return draft

        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )

    finally:
        db.close()