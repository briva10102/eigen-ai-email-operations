from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class SalesLeadExtractionRecord(Base):
    __tablename__ = "sales_lead_extractions"

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

    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(100), nullable=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    product_interest: Mapped[str | None] = mapped_column(Text, nullable=True)
    budget: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timeline: Mapped[str | None] = mapped_column(String(255), nullable=True)
    requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
    urgency: Mapped[str | None] = mapped_column(String(100), nullable=True)

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )