"""Unit of Work implementation."""

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces import IIncidentRepository, IUnitOfWork
from app.infrastructure.repository import IncidentRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    """SQLAlchemy implementation of Unit of Work pattern."""

    def __init__(self, session: AsyncSession):
        self._session = session
        self.incidents: IIncidentRepository = IncidentRepository(session)

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager."""
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        """Commit the transaction."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Rollback the transaction."""
        await self._session.rollback()
