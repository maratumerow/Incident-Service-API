"""SQLAlchemy models."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class IncidentModel(Base):
    """SQLAlchemy model for Incident."""

    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        nullable=False,
    )
