"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr


# =============================================================================
# Legacy Schemas (kept for backward compatibility)
# =============================================================================

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

    status: str = Field(default="pending", pattern="^(draft|pending|approved|rejected)$")


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


# =============================================================================
# Enterprise AI Governance Intake Schemas
# =============================================================================

# -----------------------------------------------------------------------------
# Section 1: AI System Inventory
# -----------------------------------------------------------------------------

class Section1Inventory(BaseModel):
    """AI System Inventory fields."""
    system_name: Optional[str] = Field(None, max_length=255)
    business_purpose: Optional[str] = None
    build_vs_buy: Optional[str] = Field(None, pattern="^(build|buy|hybrid)$")
    vendor_name: Optional[str] = Field(None, max_length=255)
    deployment_status: Optional[str] = Field(
        None,
        pattern="^(planning|pilot|limited_production|full_production|deprecated)$"
    )
    user_count: Optional[int] = Field(None, ge=0)
    human_in_the_loop: Optional[str] = Field(
        None,
        pattern="^(full_oversight|approval_required|exception_only|none)$"
    )
    integration_points: Optional[List[str]] = None
    technical_constraints: Optional[str] = None


# -----------------------------------------------------------------------------
# Section 2: Decision Impact Classification
# -----------------------------------------------------------------------------

class RiskFlagAcknowledgment(BaseModel):
    """Individual risk flag acknowledgment."""
    acknowledged: bool = False
    notes: Optional[str] = None


class Section2DecisionImpact(BaseModel):
    """Decision Impact Classification fields."""
    decision_classification: Optional[str] = Field(
        None,
        pattern="^(informational|decision_support|semi_autonomous|fully_autonomous)$"
    )
    output_usage_description: Optional[str] = None
    risk_flags: Optional[Dict[str, RiskFlagAcknowledgment]] = None


# -----------------------------------------------------------------------------
# Section 3: Data Sensitivity & Flow
# -----------------------------------------------------------------------------

class Section3DataSensitivity(BaseModel):
    """Data Sensitivity & Flow fields."""
    approved_data_types: Optional[List[str]] = None
    prohibited_data_types: Optional[List[str]] = None
    user_awareness_training: Optional[bool] = None
    user_awareness_attestation: Optional[bool] = None
    technical_prevention_measures: Optional[List[str]] = None
    data_retention_policy: Optional[str] = Field(
        None,
        pattern="^(zero_retention|30_days|90_days|1_year|indefinite)$"
    )
    data_retention_details: Optional[str] = None
    data_egress_risk: Optional[str] = Field(None, pattern="^(none|low|medium|high)$")
    data_egress_notes: Optional[str] = None


# -----------------------------------------------------------------------------
# Section 4: Ownership & Accountability
# -----------------------------------------------------------------------------

class Section4Ownership(BaseModel):
    """Ownership & Accountability fields."""
    approving_authority: Optional[str] = Field(None, max_length=255)
    approving_authority_title: Optional[str] = Field(None, max_length=255)
    approving_authority_email: Optional[str] = Field(None, max_length=255)
    business_owner: Optional[str] = Field(None, max_length=255)
    business_owner_email: Optional[str] = Field(None, max_length=255)
    technical_owner: Optional[str] = Field(None, max_length=255)
    technical_owner_email: Optional[str] = Field(None, max_length=255)
    access_control_owner: Optional[str] = Field(None, max_length=255)
    risk_oversight_owner: Optional[str] = Field(None, max_length=255)


# -----------------------------------------------------------------------------
# Section 5: Regulatory & Contractual Context
# -----------------------------------------------------------------------------

class Section5Regulatory(BaseModel):
    """Regulatory & Contractual Context fields."""
    federal_contracts: Optional[bool] = None
    federal_contract_types: Optional[List[str]] = None
    federal_contract_details: Optional[str] = None
    tenant_segregation: Optional[bool] = None
    tenant_segregation_details: Optional[str] = None
    contract_clause_restrictions: Optional[List[str]] = None
    workforce_impact: Optional[str] = Field(
        None,
        pattern="^(none|minimal|moderate|significant)$"
    )
    workforce_impact_details: Optional[str] = None
    customer_impact: Optional[str] = Field(
        None,
        pattern="^(none|minimal|moderate|significant)$"
    )
    customer_impact_details: Optional[str] = None


# -----------------------------------------------------------------------------
# Section 6: Monitoring, Logging & Incident Response
# -----------------------------------------------------------------------------

class EscalationContact(BaseModel):
    """Escalation contact information."""
    name: str
    role: str
    email: Optional[str] = None


class Section6Monitoring(BaseModel):
    """Monitoring, Logging & Incident Response fields."""
    usage_logging_enabled: Optional[bool] = None
    usage_logging_details: Optional[str] = None
    logging_access_owner: Optional[str] = Field(None, max_length=255)
    compliance_visibility: Optional[bool] = None
    compliance_visibility_details: Optional[str] = None
    misuse_detection_capability: Optional[bool] = None
    misuse_detection_details: Optional[str] = None
    incident_response_documented: Optional[bool] = None
    incident_response_path: Optional[str] = None
    escalation_contacts: Optional[List[EscalationContact]] = None


# -----------------------------------------------------------------------------
# Section 7: Risk Assessment (related table)
# -----------------------------------------------------------------------------

class RiskAssessmentCreate(BaseModel):
    """Create a risk assessment item."""
    risk_category: str = Field(..., max_length=100)
    risk_description: str = Field(..., min_length=1)
    is_mitigated: bool = False
    mitigation_status: Optional[str] = Field(
        None,
        pattern="^(complete|in_progress|planned|not_planned)$"
    )
    mitigation_details: Optional[str] = None
    residual_risk_level: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    residual_exposure: Optional[str] = None


class RiskAssessmentUpdate(BaseModel):
    """Update a risk assessment item."""
    risk_category: Optional[str] = Field(None, max_length=100)
    risk_description: Optional[str] = Field(None, min_length=1)
    is_mitigated: Optional[bool] = None
    mitigation_status: Optional[str] = Field(
        None,
        pattern="^(complete|in_progress|planned|not_planned)$"
    )
    mitigation_details: Optional[str] = None
    residual_risk_level: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    residual_exposure: Optional[str] = None


class RiskAssessmentResponse(RiskAssessmentCreate):
    """Risk assessment response."""
    id: int
    intake_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# Section 8: Governance Gaps & Required Artifacts
# -----------------------------------------------------------------------------

class RequiredArtifactCreate(BaseModel):
    """Create a required artifact."""
    gap_description: Optional[str] = None
    artifact_type: str = Field(..., max_length=100)
    artifact_name: str = Field(..., min_length=1, max_length=255)
    owner: Optional[str] = Field(None, max_length=255)
    owner_email: Optional[str] = Field(None, max_length=255)
    due_date: Optional[datetime] = None
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed|waived)$")
    notes: Optional[str] = None


class RequiredArtifactUpdate(BaseModel):
    """Update a required artifact."""
    gap_description: Optional[str] = None
    artifact_type: Optional[str] = Field(None, max_length=100)
    artifact_name: Optional[str] = Field(None, min_length=1, max_length=255)
    owner: Optional[str] = Field(None, max_length=255)
    owner_email: Optional[str] = Field(None, max_length=255)
    due_date: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed|waived)$")
    notes: Optional[str] = None


class RequiredArtifactResponse(RequiredArtifactCreate):
    """Required artifact response."""
    id: int
    intake_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# Section 9: Readiness Determination
# -----------------------------------------------------------------------------

class Section9Readiness(BaseModel):
    """Readiness Determination fields."""
    readiness_status: Optional[str] = Field(
        None,
        pattern="^(approved|conditional|not_ready)$"
    )
    conditions_for_approval: Optional[List[str]] = None
    restrictions: Optional[List[str]] = None
    recommended_phase: Optional[str] = Field(
        None,
        pattern="^(pilot_continuation|governance_design|expansion)$"
    )
    readiness_notes: Optional[str] = None


# -----------------------------------------------------------------------------
# Section 10: Action Items (related table)
# -----------------------------------------------------------------------------

class ActionItemCreate(BaseModel):
    """Create an action item."""
    action_description: str = Field(..., min_length=1)
    responsible_party: Optional[str] = Field(None, max_length=255)
    responsible_party_email: Optional[str] = Field(None, max_length=255)
    urgency_level: str = Field(default="medium", pattern="^(immediate|high|medium|low)$")
    due_date: Optional[datetime] = None
    notes: Optional[str] = None


class ActionItemUpdate(BaseModel):
    """Update an action item."""
    action_description: Optional[str] = Field(None, min_length=1)
    responsible_party: Optional[str] = Field(None, max_length=255)
    responsible_party_email: Optional[str] = Field(None, max_length=255)
    urgency_level: Optional[str] = Field(None, pattern="^(immediate|high|medium|low)$")
    due_date: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed)$")
    notes: Optional[str] = None


class ActionItemResponse(ActionItemCreate):
    """Action item response."""
    id: int
    intake_id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# Main Intake Schemas
# -----------------------------------------------------------------------------

class IntakeCreate(BaseModel):
    """Create a new intake (minimal data to start)."""
    system_name: str = Field(..., min_length=1, max_length=255)
    business_owner: Optional[str] = Field(None, max_length=255)
    business_owner_email: Optional[str] = Field(None, max_length=255)


class IntakeSectionUpdate(BaseModel):
    """Update intake - section-based for autosave.

    Each section is optional, allowing partial updates.
    """
    section_1: Optional[Section1Inventory] = None
    section_2: Optional[Section2DecisionImpact] = None
    section_3: Optional[Section3DataSensitivity] = None
    section_4: Optional[Section4Ownership] = None
    section_5: Optional[Section5Regulatory] = None
    section_6: Optional[Section6Monitoring] = None
    section_9: Optional[Section9Readiness] = None
    identified_gaps: Optional[List[str]] = None
    current_step: Optional[int] = Field(None, ge=1, le=10)


class IntakeListItem(BaseModel):
    """Intake list item for dashboard/list views."""
    id: int
    system_name: Optional[str]
    business_owner: Optional[str]
    intake_status: str
    current_step: int
    computed_risk_tier: Optional[str]
    readiness_status: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IntakeResponse(BaseModel):
    """Full intake response with all data."""
    id: int

    # Section 1
    system_name: Optional[str] = None
    business_purpose: Optional[str] = None
    build_vs_buy: Optional[str] = None
    vendor_name: Optional[str] = None
    deployment_status: Optional[str] = None
    user_count: Optional[int] = None
    human_in_the_loop: Optional[str] = None
    integration_points: Optional[List[str]] = None
    technical_constraints: Optional[str] = None

    # Section 2
    decision_classification: Optional[str] = None
    output_usage_description: Optional[str] = None
    risk_flags: Optional[Dict[str, Any]] = None

    # Section 3
    approved_data_types: Optional[List[str]] = None
    prohibited_data_types: Optional[List[str]] = None
    user_awareness_training: Optional[bool] = None
    user_awareness_attestation: Optional[bool] = None
    technical_prevention_measures: Optional[List[str]] = None
    data_retention_policy: Optional[str] = None
    data_retention_details: Optional[str] = None
    data_egress_risk: Optional[str] = None
    data_egress_notes: Optional[str] = None

    # Section 4
    approving_authority: Optional[str] = None
    approving_authority_title: Optional[str] = None
    approving_authority_email: Optional[str] = None
    business_owner: Optional[str] = None
    business_owner_email: Optional[str] = None
    technical_owner: Optional[str] = None
    technical_owner_email: Optional[str] = None
    access_control_owner: Optional[str] = None
    risk_oversight_owner: Optional[str] = None

    # Section 5
    federal_contracts: Optional[bool] = None
    federal_contract_types: Optional[List[str]] = None
    federal_contract_details: Optional[str] = None
    tenant_segregation: Optional[bool] = None
    tenant_segregation_details: Optional[str] = None
    contract_clause_restrictions: Optional[List[str]] = None
    workforce_impact: Optional[str] = None
    workforce_impact_details: Optional[str] = None
    customer_impact: Optional[str] = None
    customer_impact_details: Optional[str] = None

    # Section 6
    usage_logging_enabled: Optional[bool] = None
    usage_logging_details: Optional[str] = None
    logging_access_owner: Optional[str] = None
    compliance_visibility: Optional[bool] = None
    compliance_visibility_details: Optional[str] = None
    misuse_detection_capability: Optional[bool] = None
    misuse_detection_details: Optional[str] = None
    incident_response_documented: Optional[bool] = None
    incident_response_path: Optional[str] = None
    escalation_contacts: Optional[List[Dict[str, str]]] = None

    # Section 8
    identified_gaps: Optional[List[str]] = None

    # Section 9
    readiness_status: Optional[str] = None
    conditions_for_approval: Optional[List[str]] = None
    restrictions: Optional[List[str]] = None
    recommended_phase: Optional[str] = None
    readiness_notes: Optional[str] = None
    readiness_computed_at: Optional[datetime] = None

    # Metadata
    intake_status: str
    current_step: int
    section_completion: Optional[Dict[str, bool]] = None
    computed_risk_tier: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime] = None
    last_autosave_at: Optional[datetime] = None

    # Related data
    risk_assessments: List[RiskAssessmentResponse] = []
    required_artifacts: List[RequiredArtifactResponse] = []
    action_items: List[ActionItemResponse] = []

    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# Readiness Report Schema
# -----------------------------------------------------------------------------

class ReadinessReportSummary(BaseModel):
    """Executive summary for readiness report."""
    system_name: str
    business_purpose: Optional[str]
    deployment_status: Optional[str]
    decision_classification: Optional[str]
    readiness_status: str
    risk_tier: Optional[str]
    key_owners: Dict[str, Optional[str]]
    risk_counts: Dict[str, int]
    pending_actions_count: int


class ReadinessReport(BaseModel):
    """Full readiness report structure."""
    intake_id: int
    system_name: str
    generated_at: datetime

    # Summary
    executive_summary: ReadinessReportSummary

    # Section details
    section_summaries: Dict[str, Dict[str, Any]]

    # Key findings
    mitigated_risks: List[RiskAssessmentResponse]
    unmitigated_risks: List[RiskAssessmentResponse]
    governance_gaps: List[str]
    pending_artifacts: List[RequiredArtifactResponse]

    # Determination
    readiness_status: str
    conditions_for_approval: List[str]
    restrictions: List[str]
    recommended_phase: Optional[str]

    # Actions
    action_items: List[ActionItemResponse]
