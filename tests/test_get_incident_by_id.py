"""Tests for GET /incidents/{incident_id} endpoint."""

import pytest
from httpx import AsyncClient

from app.domain.enums import IncidentSource, IncidentStatus


@pytest.mark.asyncio
async def test_get_incident_by_id_success(client: AsyncClient) -> None:
    """Test getting incident by ID successfully."""
    # Create incident
    create_response = await client.post(
        "/incidents",
        json={
            "description": "Database connection lost",
            "status": IncidentStatus.OPEN.value,
            "source": IncidentSource.MONITORING.value,
        },
    )
    incident_id = create_response.json()["id"]

    # Get incident by ID
    response = await client.get(f"/incidents/{incident_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == incident_id
    assert data["description"] == "Database connection lost"
    assert data["status"] == IncidentStatus.OPEN.value


@pytest.mark.asyncio
async def test_get_incident_by_id_not_found(client: AsyncClient) -> None:
    """Test getting non-existent incident."""
    response = await client.get("/incidents/999")

    assert response.status_code == 404
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_get_specific_incident_among_multiple(
    client: AsyncClient,
) -> None:
    """Test getting specific incident when multiple exist."""
    # Create multiple incidents
    incidents_data = []
    for i in range(3):
        create_response = await client.post(
            "/incidents",
            json={
                "description": f"Incident {i}",
                "status": IncidentStatus.OPEN.value,
                "source": IncidentSource.MONITORING.value,
            },
        )
        incidents_data.append(create_response.json())

    # Get second incident
    target_id = incidents_data[1]["id"]
    response = await client.get(f"/incidents/{target_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == target_id
    assert data["description"] == "Incident 1"
