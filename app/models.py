"""SQLAlchemy ORM models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


# =============================================================================
# Legacy Model (kept for backward compatibility)
# =============================================================================

class UseCase(Base):
    """Legacy use case database model - kept for backward compatibility."""

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


# =============================================================================
# Enterprise AI Governance Intake Models
# =============================================================================

class Intake(Base):
    """Main governance intake record - comprehensive AI system assessment."""

    __tablename__ = "intakes"

    id = Column(Integer, primary_key=True, index=True)

    # -------------------------------------------------------------------------
    # Section 1: AI System Inventory
    # -------------------------------------------------------------------------
    system_name = Column(String(255))
    business_purpose = Column(Text)
    build_vs_buy = Column(String(50))  # "build", "buy", "hybrid"
    vendor_name = Column(String(255))
    deployment_status = Column(String(50))  # "planning", "pilot", "limited_production", "full_production", "deprecated"
    user_count = Column(Integer)
    human_in_the_loop = Column(String(100))  # "full_oversight", "approval_required", "exception_only", "none"
    integration_points = Column(JSON, default=list)  # List of system integrations
    technical_constraints = Column(Text)

    # -------------------------------------------------------------------------
    # Section 2: Decision Impact Classification
    # -------------------------------------------------------------------------
    decision_classification = Column(String(50))  # "informational", "decision_support", "semi_autonomous", "fully_autonomous"
    output_usage_description = Column(Text)
    risk_flags = Column(JSON, default=dict)  # {"flag_name": {"acknowledged": bool, "notes": str}}

    # -------------------------------------------------------------------------
    # Section 3: Data Sensitivity & Flow
    # -------------------------------------------------------------------------
    approved_data_types = Column(JSON, default=list)
    prohibited_data_types = Column(JSON, default=list)
    user_awareness_training = Column(Boolean, default=False)
    user_awareness_attestation = Column(Boolean, default=False)
    technical_prevention_measures = Column(JSON, default=list)
    data_retention_policy = Column(String(100))  # "zero_retention", "30_days", "90_days", "1_year", "indefinite"
    data_retention_details = Column(Text)
    data_egress_risk = Column(String(50))  # "none", "low", "medium", "high"
    data_egress_notes = Column(Text)

    # -------------------------------------------------------------------------
    # Section 4: Ownership & Accountability
    # -------------------------------------------------------------------------
    approving_authority = Column(String(255))
    approving_authority_title = Column(String(255))
    approving_authority_email = Column(String(255))
    business_owner = Column(String(255))
    business_owner_email = Column(String(255))
    technical_owner = Column(String(255))
    technical_owner_email = Column(String(255))
    access_control_owner = Column(String(255))
    risk_oversight_owner = Column(String(255))

    # -------------------------------------------------------------------------
    # Section 5: Regulatory & Contractual Context
    # -------------------------------------------------------------------------
    federal_contracts = Column(Boolean, default=False)
    federal_contract_types = Column(JSON, default=list)  # ["DFARS", "CMMC", "FedRAMP", etc.]
    federal_contract_details = Column(Text)
    tenant_segregation = Column(Boolean)
    tenant_segregation_details = Column(Text)
    contract_clause_restrictions = Column(JSON, default=list)
    workforce_impact = Column(String(50))  # "none", "minimal", "moderate", "significant"
    workforce_impact_details = Column(Text)
    customer_impact = Column(String(50))  # "none", "minimal", "moderate", "significant"
    customer_impact_details = Column(Text)

    # -------------------------------------------------------------------------
    # Section 6: Monitoring, Logging & Incident Response
    # -------------------------------------------------------------------------
    usage_logging_enabled = Column(Boolean, default=False)
    usage_logging_details = Column(Text)
    logging_access_owner = Column(String(255))
    compliance_visibility = Column(Boolean, default=False)
    compliance_visibility_details = Column(Text)
    misuse_detection_capability = Column(Boolean, default=False)
    misuse_detection_details = Column(Text)
    incident_response_documented = Column(Boolean, default=False)
    incident_response_path = Column(Text)
    escalation_contacts = Column(JSON, default=list)  # [{"name": str, "role": str, "email": str}]

    # -------------------------------------------------------------------------
    # Section 7: Residual Risk Assessment (stored in related table)
    # -------------------------------------------------------------------------
    # See RiskAssessment model below

    # -------------------------------------------------------------------------
    # Section 8: Governance Gaps & Required Artifacts
    # -------------------------------------------------------------------------
    identified_gaps = Column(JSON, default=list)  # List of gap descriptions
    # See RequiredArtifact model below

    # -------------------------------------------------------------------------
    # Section 9: Readiness Determination
    # -------------------------------------------------------------------------
    readiness_status = Column(String(50))  # "approved", "conditional", "not_ready", None
    conditions_for_approval = Column(JSON, default=list)
    restrictions = Column(JSON, default=list)
    recommended_phase = Column(String(100))  # "pilot_continuation", "governance_design", "expansion"
    readiness_notes = Column(Text)
    readiness_computed_at = Column(DateTime)

    # -------------------------------------------------------------------------
    # Section 10: Required Next Actions (stored in related table)
    # -------------------------------------------------------------------------
    # See ActionItem model below

    # -------------------------------------------------------------------------
    # Metadata & Tracking
    # -------------------------------------------------------------------------
    intake_status = Column(String(50), default="draft")  # "draft", "submitted", "under_review", "completed"
    current_step = Column(Integer, default=1)  # Wizard progress (1-10)
    section_completion = Column(JSON, default=dict)  # {"1": true, "2": false, ...}
    computed_risk_tier = Column(String(20))  # "low", "medium", "high"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = Column(DateTime)
    last_autosave_at = Column(DateTime)

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------
    risk_assessments = relationship("RiskAssessment", back_populates="intake", cascade="all, delete-orphan")
    required_artifacts = relationship("RequiredArtifact", back_populates="intake", cascade="all, delete-orphan")
    action_items = relationship("ActionItem", back_populates="intake", cascade="all, delete-orphan")


class RiskAssessment(Base):
    """Individual risk items for Section 7 - Residual Risk Assessment."""

    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    intake_id = Column(Integer, ForeignKey("intakes.id"), nullable=False)

    risk_category = Column(String(100))  # "environment_segregation", "identity_trust", "data_exposure", etc.
    risk_description = Column(Text, nullable=False)
    is_mitigated = Column(Boolean, default=False)
    mitigation_status = Column(String(50))  # "complete", "in_progress", "planned", "not_planned"
    mitigation_details = Column(Text)
    residual_risk_level = Column(String(20))  # "low", "medium", "high"
    residual_exposure = Column(Text)  # Description of remaining risk
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    intake = relationship("Intake", back_populates="risk_assessments")


class RequiredArtifact(Base):
    """Governance artifacts required for Section 8."""

    __tablename__ = "required_artifacts"

    id = Column(Integer, primary_key=True, index=True)
    intake_id = Column(Integer, ForeignKey("intakes.id"), nullable=False)

    gap_description = Column(Text)  # The governance gap this artifact addresses
    artifact_type = Column(String(100))  # "incident_playbook", "raci_assignment", "usage_guidance", etc.
    artifact_name = Column(String(255), nullable=False)
    owner = Column(String(255))
    owner_email = Column(String(255))
    due_date = Column(DateTime)
    status = Column(String(50), default="pending")  # "pending", "in_progress", "completed", "waived"
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    intake = relationship("Intake", back_populates="required_artifacts")


class ActionItem(Base):
    """Action items for Section 10 - Required Next Actions."""

    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    intake_id = Column(Integer, ForeignKey("intakes.id"), nullable=False)

    action_description = Column(Text, nullable=False)
    responsible_party = Column(String(255))
    responsible_party_email = Column(String(255))
    urgency_level = Column(String(20), default="medium")  # "immediate", "high", "medium", "low"
    due_date = Column(DateTime)
    status = Column(String(50), default="pending")  # "pending", "in_progress", "completed"
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationship
    intake = relationship("Intake", back_populates="action_items")
