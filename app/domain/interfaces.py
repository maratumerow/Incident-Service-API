"""Repository interfaces (ports)."""

from abc import ABC, abstractmethod
from types import TracebackType

from app.domain.entities import Incident
from app.domain.enums import IncidentStatus


class IIncidentRepository(ABC):
    """Interface for incident repository."""

    @abstractmethod
    async def create(self, incident: Incident) -> Incident:
        """Create a new incident."""

    @abstractmethod
    async def get_all(
        self, status: IncidentStatus | None = None
    ) -> list[Incident]:
        """Get all incidents, optionally filtered by status."""

    @abstractmethod
    async def get_by_id(self, incident_id: int) -> Incident | None:
        """Get incident by ID."""

    @abstractmethod
    async def update_status(
        self, incident_id: int, status: IncidentStatus
    ) -> Incident:
        """Update incident status."""


class IUnitOfWork(ABC):
    """Interface for Unit of Work pattern."""

    incidents: IIncidentRepository

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        """Enter async context manager."""

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager."""

    @abstractmethod
    async def commit(self) -> None:
        """Commit the transaction."""

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the transaction."""
