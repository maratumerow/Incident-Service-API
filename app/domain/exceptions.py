"""Domain exceptions."""


class DomainException(Exception):
    """Base domain exception."""


class IncidentNotFoundError(DomainException):
    """Raised when incident is not found."""

    def __init__(self, incident_id: int):
        self.incident_id = incident_id
        super().__init__(f"Incident with id {incident_id} not found")
