"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UseCaseBase(BaseModel):
    """Base schema with common fields."""

    title: str = Field(..., min_length=1, max_length=255)
    owner: str = Field(..., min_length=1, max_length=255)
    business_unit: str = Field(..., min_length=1, max_length=255)
    purpose: str = Field(..., min_length=1)
    model_type: str = Field(..., min_length=1, max_length=100)
    vendor: str = Field(..., min_length=1, max_length=255)
    data_types: list[str] = Field(default_factory=list)
    data_residency: str = Field(..., min_length=1, max_length=100)
    external_sharing: str = Field(..., pattern="^(yes|no)$")


class UseCaseCreate(UseCaseBase):
    """Schema for creating a use case."""

    status: str = Field(default="draft", pattern="^(draft|pending|approved|rejected)$")


class UseCaseUpdate(BaseModel):
    """Schema for updating a use case (all fields optional)."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    owner: Optional[str] = Field(None, min_length=1, max_length=255)
    business_unit: Optional[str] = Field(None, min_length=1, max_length=255)
    purpose: Optional[str] = Field(None, min_length=1)
    model_type: Optional[str] = Field(None, min_length=1, max_length=100)
    vendor: Optional[str] = Field(None, min_length=1, max_length=255)
    data_types: Optional[list[str]] = None
    data_residency: Optional[str] = Field(None, min_length=1, max_length=100)
    external_sharing: Optional[str] = Field(None, pattern="^(yes|no)$")
    status: Optional[str] = Field(None, pattern="^(draft|pending|approved|rejected)$")


class UseCaseResponse(UseCaseBase):
    """Schema for use case response."""

    id: int
    risk_tier: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
