from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True)

    provider_message_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    subject: Mapped[str] = mapped_column(
        String(500),
        default=""
    )

    sender: Mapped[str] = mapped_column(
        String(320)
    )

    recipients: Mapped[str] = mapped_column(
        Text
    )

    body_text: Mapped[str] = mapped_column(
        Text
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime
    )

    email_account_id: Mapped[int] = mapped_column(
        ForeignKey("email_accounts.id")
    )
    
    thread_id: Mapped[int] = mapped_column(
    ForeignKey("email_threads.id"),
    index=True
    )