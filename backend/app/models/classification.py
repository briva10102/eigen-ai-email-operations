from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base
from backend.app.schemas.classification import EmailCategory


class EmailClassificationRecord(Base):
    __tablename__ = "email_classifications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    email_id: Mapped[int] = mapped_column(
        ForeignKey("emails.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    category: Mapped[EmailCategory] = mapped_column(
        Enum(EmailCategory),
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    urgency: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    intent: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )