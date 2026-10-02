from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class EmailProvider(str, Enum):
    GMAIL = "GMAIL"


class EmailAccount(Base):
    __tablename__ = "email_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    email_address: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        index=True
    )

    provider: Mapped[EmailProvider] = mapped_column()