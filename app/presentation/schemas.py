"""Pydantic schemas for API requests and responses."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.enums import IncidentSource, IncidentStatus


class IncidentCreateRequest(BaseModel):
    """Request schema for creating an incident."""

    description: str = Field(
        ..., min_length=1, description="Incident description"
    )
    status: IncidentStatus = Field(..., description="Incident status")
    source: IncidentSource = Field(..., description="Incident source")


class IncidentStatusUpdateRequest(BaseModel):
    """Request schema for updating incident status."""

    status: IncidentStatus = Field(..., description="New incident status")


class IncidentResponse(BaseModel):
    """Response schema for incident."""

    model_config = {"from_attributes": True}

    id: int
    description: str
    status: IncidentStatus
    source: IncidentSource
    created_at: datetime


class ErrorResponse(BaseModel):
    """Error response schema."""

    detail: str
