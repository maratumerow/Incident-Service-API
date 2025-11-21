"""Domain entities."""

from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import IncidentSource, IncidentStatus


@dataclass
class Incident:
    """Incident domain entity."""

    id: int | None
    description: str
    status: IncidentStatus
    source: IncidentSource
    created_at: datetime

    def __post_init__(self) -> None:
        """Validate incident data."""
        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty")
