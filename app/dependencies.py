"""Dependency injection container."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases import (
    CreateIncidentUseCase,
    GetIncidentByIdUseCase,
    GetIncidentsUseCase,
    UpdateIncidentStatusUseCase,
)
from app.domain.interfaces import IUnitOfWork
from app.infrastructure.database import get_db
from app.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


async def get_uow(db: AsyncSession = Depends(get_db)) -> IUnitOfWork:
    """Dependency for getting Unit of Work implementation."""
    return SQLAlchemyUnitOfWork(db)


def get_create_incident_use_case(
    uow: IUnitOfWork = Depends(get_uow),
) -> CreateIncidentUseCase:
    """Dependency for CreateIncidentUseCase."""
    return CreateIncidentUseCase(uow)


def get_get_incidents_use_case(
    uow: IUnitOfWork = Depends(get_uow),
) -> GetIncidentsUseCase:
    """Dependency for GetIncidentsUseCase."""
    return GetIncidentsUseCase(uow)


def get_get_incident_by_id_use_case(
    uow: IUnitOfWork = Depends(get_uow),
) -> GetIncidentByIdUseCase:
    """Dependency for GetIncidentByIdUseCase."""
    return GetIncidentByIdUseCase(uow)


def get_update_incident_status_use_case(
    uow: IUnitOfWork = Depends(get_uow),
) -> UpdateIncidentStatusUseCase:
    """Dependency for UpdateIncidentStatusUseCase."""
    return UpdateIncidentStatusUseCase(uow)


# Type aliases for dependency injection
UnitOfWorkDep = Annotated[IUnitOfWork, Depends(get_uow)]
CreateIncidentUseCaseDep = Annotated[
    CreateIncidentUseCase, Depends(get_create_incident_use_case)
]
GetIncidentsUseCaseDep = Annotated[
    GetIncidentsUseCase, Depends(get_get_incidents_use_case)
]
GetIncidentByIdUseCaseDep = Annotated[
    GetIncidentByIdUseCase, Depends(get_get_incident_by_id_use_case)
]
UpdateIncidentStatusUseCaseDep = Annotated[
    UpdateIncidentStatusUseCase, Depends(get_update_incident_status_use_case)
]
