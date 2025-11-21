"""Tests for POST /incidents endpoint."""

import pytest
from httpx import AsyncClient

from app.domain.enums import IncidentSource, IncidentStatus


@pytest.mark.asyncio
async def test_create_incident_success(client: AsyncClient) -> None:
    """Test successful incident creation."""
    payload = {
        "description": "Server is down",
        "status": IncidentStatus.OPEN.value,
        "source": IncidentSource.MONITORING.value,
    }

    response = await client.post("/incidents", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Server is down"
    assert data["status"] == IncidentStatus.OPEN.value
    assert data["source"] == IncidentSource.MONITORING.value
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_incident_with_operator_source(
    client: AsyncClient,
) -> None:
    """Test creating incident from operator source."""
    payload = {
        "description": "User reported login issue",
        "status": IncidentStatus.IN_PROGRESS.value,
        "source": IncidentSource.OPERATOR.value,
    }

    response = await client.post("/incidents", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "User reported login issue"
    assert data["status"] == IncidentStatus.IN_PROGRESS.value
    assert data["source"] == IncidentSource.OPERATOR.value


@pytest.mark.asyncio
async def test_create_incident_validation_error(
    client: AsyncClient,
) -> None:
    """Test incident creation with invalid data."""
    payload = {
        "description": "",
        "status": IncidentStatus.OPEN.value,
        "source": IncidentSource.MONITORING.value,
    }

    response = await client.post("/incidents", json=payload)

    assert response.status_code == 422
