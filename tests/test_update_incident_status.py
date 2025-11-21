"""Tests for PATCH /incidents/{incident_id}/status endpoint."""

import pytest
from httpx import AsyncClient

from app.domain.enums import IncidentSource, IncidentStatus


@pytest.mark.asyncio
async def test_update_incident_status_success(client: AsyncClient) -> None:
    """Test successful status update."""
    # Create incident
    create_response = await client.post(
        "/incidents",
        json={
            "description": "Network issue",
            "status": IncidentStatus.OPEN.value,
            "source": IncidentSource.MONITORING.value,
        },
    )
    incident_id = create_response.json()["id"]

    # Update status
    response = await client.patch(
        f"/incidents/{incident_id}/status",
        json={"status": IncidentStatus.IN_PROGRESS.value},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == incident_id
    assert data["status"] == IncidentStatus.IN_PROGRESS.value
    assert data["description"] == "Network issue"


@pytest.mark.asyncio
async def test_update_incident_status_to_closed(
    client: AsyncClient,
) -> None:
    """Test updating incident status to closed."""
    # Create incident in progress
    create_response = await client.post(
        "/incidents",
        json={
            "description": "Bug fix in progress",
            "status": IncidentStatus.IN_PROGRESS.value,
            "source": IncidentSource.OPERATOR.value,
        },
    )
    incident_id = create_response.json()["id"]

    # Close incident
    response = await client.patch(
        f"/incidents/{incident_id}/status",
        json={"status": IncidentStatus.CLOSED.value},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == IncidentStatus.CLOSED.value


@pytest.mark.asyncio
async def test_update_status_incident_not_found(
    client: AsyncClient,
) -> None:
    """Test updating status of non-existent incident."""
    response = await client.patch(
        "/incidents/999/status",
        json={"status": IncidentStatus.CLOSED.value},
    )

    assert response.status_code == 404
    assert "detail" in response.json()
