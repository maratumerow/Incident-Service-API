"""Tests for GET /incidents endpoint."""

import pytest
from httpx import AsyncClient

from app.domain.enums import IncidentSource, IncidentStatus


@pytest.mark.asyncio
async def test_get_all_incidents_empty(client: AsyncClient) -> None:
    """Test getting incidents when database is empty."""
    response = await client.get("/incidents")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_all_incidents(client: AsyncClient) -> None:
    """Test getting all incidents."""
    # Create incidents
    incidents = [
        {
            "description": "First incident",
            "status": IncidentStatus.OPEN.value,
            "source": IncidentSource.MONITORING.value,
        },
        {
            "description": "Second incident",
            "status": IncidentStatus.CLOSED.value,
            "source": IncidentSource.OPERATOR.value,
        },
    ]

    for incident in incidents:
        await client.post("/incidents", json=incident)

    response = await client.get("/incidents")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_incidents_filtered_by_status(
    client: AsyncClient,
) -> None:
    """Test getting incidents filtered by status."""
    # Create incidents with different statuses
    await client.post(
        "/incidents",
        json={
            "description": "Open incident",
            "status": IncidentStatus.OPEN.value,
            "source": IncidentSource.MONITORING.value,
        },
    )
    await client.post(
        "/incidents",
        json={
            "description": "Closed incident",
            "status": IncidentStatus.CLOSED.value,
            "source": IncidentSource.OPERATOR.value,
        },
    )

    response = await client.get(
        "/incidents", params={"status": IncidentStatus.OPEN.value}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == IncidentStatus.OPEN.value
    assert data[0]["description"] == "Open incident"
