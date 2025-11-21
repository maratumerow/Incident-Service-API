"""Use cases for incident management."""

from datetime import UTC, datetime

from app.domain.entities import Incident
from app.domain.enums import IncidentSource, IncidentStatus
from app.domain.exceptions import IncidentNotFoundError
from app.domain.interfaces import IUnitOfWork


class CreateIncidentUseCase:
    """Use case for creating a new incident."""

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        description: str,
        status: IncidentStatus,
        source: IncidentSource,
    ) -> Incident:
        """Create a new incident."""
        incident = Incident(
            id=None,
            description=description,
            status=status,
            source=source,
            created_at=datetime.now(UTC),
        )

        async with self.uow:
            return await self.uow.incidents.create(incident)


class GetIncidentsUseCase:
    """Use case for getting list of incidents."""

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(
        self, status: IncidentStatus | None = None
    ) -> list[Incident]:
        """Get all incidents, optionally filtered by status."""
        async with self.uow:
            return await self.uow.incidents.get_all(status)


class GetIncidentByIdUseCase:
    """Use case for getting incident by ID."""

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, incident_id: int) -> Incident:
        """Get incident by ID."""
        async with self.uow:
            incident = await self.uow.incidents.get_by_id(incident_id)

            if incident is None:
                raise IncidentNotFoundError(incident_id)

            return incident


class UpdateIncidentStatusUseCase:
    """Use case for updating incident status."""

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(
        self, incident_id: int, status: IncidentStatus
    ) -> Incident:
        """Update incident status."""
        async with self.uow:
            return await self.uow.incidents.update_status(incident_id, status)
