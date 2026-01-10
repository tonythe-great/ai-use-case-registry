"""SQLAlchemy ORM models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON

from app.db import Base


class UseCase(Base):
    """Use case database model."""

    __tablename__ = "usecases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)
    business_unit = Column(String(255), nullable=False)
    purpose = Column(Text, nullable=False)
    model_type = Column(String(100), nullable=False)
    vendor = Column(String(255), nullable=False)
    data_types = Column(JSON, default=list)
    data_residency = Column(String(100), nullable=False)
    external_sharing = Column(String(50), nullable=False)
    risk_tier = Column(String(20), nullable=False)
    status = Column(String(50), default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
