"""FastAPI routes for incidents."""

from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies import (
    CreateIncidentUseCaseDep,
    GetIncidentByIdUseCaseDep,
    GetIncidentsUseCaseDep,
    UpdateIncidentStatusUseCaseDep,
)
from app.domain.enums import IncidentStatus
from app.domain.exceptions import IncidentNotFoundError
from app.presentation.schemas import (
    IncidentCreateRequest,
    IncidentResponse,
    IncidentStatusUpdateRequest,
)

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new incident",
)
async def create_incident(
    request: IncidentCreateRequest,
    use_case: CreateIncidentUseCaseDep,
) -> IncidentResponse:
    """Create a new incident."""
    incident = await use_case.execute(
        description=request.description,
        status=request.status,
        source=request.source,
    )

    return IncidentResponse(
        id=incident.id,  # type: ignore[arg-type]
        description=incident.description,
        status=incident.status,
        source=incident.source,
        created_at=incident.created_at,
    )


@router.get(
    "",
    response_model=list[IncidentResponse],
    summary="Get list of incidents",
)
async def get_incidents(
    use_case: GetIncidentsUseCaseDep,
    status: IncidentStatus | None = Query(
        None, description="Filter by incident status"
    ),
) -> list[IncidentResponse]:
    """Get all incidents, optionally filtered by status."""
    incidents = await use_case.execute(status=status)

    return [
        IncidentResponse(
            id=incident.id,  # type: ignore[arg-type]
            description=incident.description,
            status=incident.status,
            source=incident.source,
            created_at=incident.created_at,
        )
        for incident in incidents
    ]


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
    summary="Get incident by ID",
)
async def get_incident(
    incident_id: int,
    use_case: GetIncidentByIdUseCaseDep,
) -> IncidentResponse:
    """Get a single incident by ID."""
    try:
        incident = await use_case.execute(incident_id)
    except IncidentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return IncidentResponse(
        id=incident.id,  # type: ignore[arg-type]
        description=incident.description,
        status=incident.status,
        source=incident.source,
        created_at=incident.created_at,
    )


@router.patch(
    "/{incident_id}/status",
    response_model=IncidentResponse,
    summary="Update incident status",
)
async def update_incident_status(
    incident_id: int,
    request: IncidentStatusUpdateRequest,
    use_case: UpdateIncidentStatusUseCaseDep,
) -> IncidentResponse:
    """Update the status of an incident."""
    try:
        incident = await use_case.execute(incident_id, request.status)
    except IncidentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return IncidentResponse(
        id=incident.id,  # type: ignore[arg-type]
        description=incident.description,
        status=incident.status,
        source=incident.source,
        created_at=incident.created_at,
    )
