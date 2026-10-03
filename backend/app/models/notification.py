from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    email_id: Mapped[int | None] = mapped_column(
        ForeignKey("emails.id"),
        nullable=True,
        index=True,
    )

    workflow_run_id: Mapped[int | None] = mapped_column(
        ForeignKey("workflow_runs.id"),
        nullable=True,
        index=True,
    )

    recipient: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="UNREAD",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )