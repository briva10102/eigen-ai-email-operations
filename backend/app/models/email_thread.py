from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class EmailThread(Base):
    __tablename__ = "email_threads"

    id: Mapped[int] = mapped_column(primary_key=True)

    provider_thread_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    subject: Mapped[str] = mapped_column(
        String(500),
        default=""
    )