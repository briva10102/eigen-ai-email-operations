from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class EmailDraft(Base):
    __tablename__ = "email_drafts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    email_id: Mapped[int] = mapped_column(
        ForeignKey("emails.id"),
        nullable=False,
        index=True,
    )

    workflow_run_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_runs.id"),
        nullable=False,
        index=True,
    )

    subject: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PENDING_REVIEW",
    )
    
    sent_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True),
    nullable=True,
    )

    provider_message_id: Mapped[str | None] = mapped_column(
    String(255),
    nullable=True,
    )

    reviewed_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )