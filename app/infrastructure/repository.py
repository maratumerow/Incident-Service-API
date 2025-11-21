"""Incident repository implementation."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Incident
from app.domain.enums import IncidentSource, IncidentStatus
from app.domain.exceptions import IncidentNotFoundError
from app.domain.interfaces import IIncidentRepository
from app.infrastructure.models import IncidentModel


class IncidentRepository(IIncidentRepository):
    """SQLAlchemy implementation of incident repository."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, incident: Incident) -> Incident:
        """Create a new incident."""
        db_incident = IncidentModel(
            description=incident.description,
            status=incident.status.value,
            source=incident.source.value,
            created_at=incident.created_at,
        )
        self.db.add(db_incident)
        await self.db.flush()

        return self._to_entity(db_incident)

    async def get_all(
        self, status: IncidentStatus | None = None
    ) -> list[Incident]:
        """Get all incidents, optionally filtered by status."""
        stmt = select(IncidentModel).order_by(IncidentModel.created_at.desc())

        if status is not None:
            stmt = stmt.filter(IncidentModel.status == status.value)

        result = await self.db.execute(stmt)
        db_incidents = result.scalars().all()
        return [self._to_entity(db_incident) for db_incident in db_incidents]

    async def get_by_id(self, incident_id: int) -> Incident | None:
        """Get incident by ID."""
        stmt = select(IncidentModel).filter(IncidentModel.id == incident_id)
        result = await self.db.execute(stmt)
        db_incident = result.scalar_one_or_none()

        if db_incident is None:
            return None

        return self._to_entity(db_incident)

    async def update_status(
        self, incident_id: int, status: IncidentStatus
    ) -> Incident:
        """Update incident status."""
        stmt = (
            select(IncidentModel)
            .filter(IncidentModel.id == incident_id)
            .with_for_update()
        )
        result = await self.db.execute(stmt)
        db_incident = result.scalar_one_or_none()

        if db_incident is None:
            raise IncidentNotFoundError(incident_id)

        db_incident.status = status.value
        await self.db.flush()

        return self._to_entity(db_incident)

    @staticmethod
    def _to_entity(db_incident: IncidentModel) -> Incident:
        """Convert database model to domain entity."""
        return Incident(
            id=db_incident.id,
            description=db_incident.description,
            status=IncidentStatus(db_incident.status),
            source=IncidentSource(db_incident.source),
            created_at=db_incident.created_at,
        )
