"""Domain enums for incident status and source."""

from enum import Enum


class IncidentStatus(str, Enum):
    """Incident status enumeration."""

    OPEN = "открыт"
    IN_PROGRESS = "в работе"
    CLOSED = "закрыт"


class IncidentSource(str, Enum):
    """Incident source enumeration."""

    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"
