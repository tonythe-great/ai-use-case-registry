"""FastAPI application for AI Use-Case Registry & Governance Intake."""

from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import engine, get_db, Base
from app.models import UseCase, Intake, RiskAssessment, RequiredArtifact, ActionItem
from app.schemas import (
    # Legacy schemas
    UseCaseCreate, UseCaseUpdate, UseCaseResponse,
    # Intake schemas
    IntakeCreate, IntakeSectionUpdate, IntakeListItem, IntakeResponse,
    RiskAssessmentCreate, RiskAssessmentUpdate, RiskAssessmentResponse,
    RequiredArtifactCreate, RequiredArtifactUpdate, RequiredArtifactResponse,
    ActionItemCreate, ActionItemUpdate, ActionItemResponse,
)
from app.risk import compute_risk_tier

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Governance Intake System",
    description="Enterprise AI governance intake and use case registry",
    version="2.0.0",
)

templates = Jinja2Templates(directory="app/templates")


# =============================================================================
# Helper Functions
# =============================================================================

def compute_section_completion(intake: Intake) -> dict:
    """Compute which sections are complete based on required fields."""
    completion = {}

    # Section 1: AI System Inventory (required: system_name, business_purpose)
    completion["1"] = bool(intake.system_name and intake.business_purpose)

    # Section 2: Decision Impact (required: decision_classification)
    completion["2"] = bool(intake.decision_classification)

    # Section 3: Data Sensitivity (required: at least one data type selected)
    completion["3"] = bool(intake.approved_data_types or intake.prohibited_data_types)

    # Section 4: Ownership (required: approving_authority, business_owner, technical_owner)
    completion["4"] = bool(
        intake.approving_authority and
        intake.business_owner and
        intake.technical_owner
    )

    # Section 5: Regulatory (no required fields)
    completion["5"] = True

    # Section 6: Monitoring (no required fields, but recommended)
    completion["6"] = True

    # Section 7: Risks (check if any risks have been added)
    completion["7"] = len(intake.risk_assessments) > 0

    # Section 8: Artifacts (no required fields)
    completion["8"] = True

    # Section 9: Readiness (no required fields - computed)
    completion["9"] = True

    # Section 10: Actions (check if any actions have been added for non-ready status)
    completion["10"] = True

    return completion


def apply_section_updates(intake: Intake, updates: IntakeSectionUpdate) -> None:
    """Apply section updates to an intake record."""
    update_data = updates.model_dump(exclude_unset=True)

    for section_key, section_data in update_data.items():
        if section_key == "current_step":
            intake.current_step = section_data
        elif section_key == "identified_gaps":
            intake.identified_gaps = section_data
        elif section_data and isinstance(section_data, dict):
            # Apply individual field updates from section
            for field, value in section_data.items():
                if hasattr(intake, field):
                    setattr(intake, field, value)


# =============================================================================
# Dashboard & Legacy Routes
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Serve the executive dashboard page."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    """Serve the legacy use case registration form."""
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics for the executive view."""
    # Get all use cases (legacy)
    all_usecases = db.query(UseCase).all()
    total_count = len(all_usecases)

    # Count by risk tier
    high_risk_count = sum(1 for uc in all_usecases if uc.risk_tier == "high")
    medium_risk_count = sum(1 for uc in all_usecases if uc.risk_tier == "medium")
    low_risk_count = sum(1 for uc in all_usecases if uc.risk_tier == "low")

    # Count pending approvals
    pending_count = sum(1 for uc in all_usecases if uc.status == "pending")

    # Calculate external sharing percentage
    external_sharing_count = sum(1 for uc in all_usecases if uc.external_sharing == "yes")
    external_sharing_pct = round((external_sharing_count / total_count * 100), 1) if total_count > 0 else 0

    # Get high risk items
    high_risk_items = [
        {
            "id": uc.id,
            "title": uc.title,
            "owner": uc.owner,
            "business_unit": uc.business_unit,
            "data_types": uc.data_types,
            "status": uc.status,
            "risk_tier": uc.risk_tier,
        }
        for uc in all_usecases
        if uc.risk_tier == "high"
    ]

    # Get intake statistics
    all_intakes = db.query(Intake).all()
    intake_stats = {
        "total": len(all_intakes),
        "draft": sum(1 for i in all_intakes if i.intake_status == "draft"),
        "submitted": sum(1 for i in all_intakes if i.intake_status == "submitted"),
        "approved": sum(1 for i in all_intakes if i.readiness_status == "approved"),
        "conditional": sum(1 for i in all_intakes if i.readiness_status == "conditional"),
        "not_ready": sum(1 for i in all_intakes if i.readiness_status == "not_ready"),
    }

    return {
        "total_count": total_count,
        "high_risk_count": high_risk_count,
        "pending_count": pending_count,
        "external_sharing_pct": external_sharing_pct,
        "risk_distribution": {
            "low": low_risk_count,
            "medium": medium_risk_count,
            "high": high_risk_count,
        },
        "high_risk_items": high_risk_items,
        "intake_stats": intake_stats,
    }


# =============================================================================
# Legacy Use Case Endpoints (kept for backward compatibility)
# =============================================================================

@app.post("/usecases", response_model=UseCaseResponse, status_code=201)
def create_usecase(usecase: UseCaseCreate, db: Session = Depends(get_db)):
    """Create a new use case (legacy)."""
    risk_tier = compute_risk_tier(
        data_types=usecase.data_types,
        data_residency=usecase.data_residency,
        external_sharing=usecase.external_sharing,
    )

    db_usecase = UseCase(
        title=usecase.title,
        owner=usecase.owner,
        business_unit=usecase.business_unit,
        purpose=usecase.purpose,
        model_type=usecase.model_type,
        vendor=usecase.vendor,
        data_types=usecase.data_types,
        data_residency=usecase.data_residency,
        external_sharing=usecase.external_sharing,
        risk_tier=risk_tier,
        status=usecase.status,
    )

    db.add(db_usecase)
    db.commit()
    db.refresh(db_usecase)

    return db_usecase


@app.get("/usecases", response_model=list[UseCaseResponse])
def list_usecases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all use cases with pagination (legacy)."""
    usecases = db.query(UseCase).offset(skip).limit(limit).all()
    return usecases


@app.get("/usecases/{usecase_id}", response_model=UseCaseResponse)
def get_usecase(usecase_id: int, db: Session = Depends(get_db)):
    """Get a specific use case by ID (legacy)."""
    usecase = db.query(UseCase).filter(UseCase.id == usecase_id).first()
    if usecase is None:
        raise HTTPException(status_code=404, detail="Use case not found")
    return usecase


@app.patch("/usecases/{usecase_id}", response_model=UseCaseResponse)
def update_usecase(
    usecase_id: int,
    usecase_update: UseCaseUpdate,
    db: Session = Depends(get_db),
):
    """Update a use case (partial update, legacy)."""
    usecase = db.query(UseCase).filter(UseCase.id == usecase_id).first()
    if usecase is None:
        raise HTTPException(status_code=404, detail="Use case not found")

    update_data = usecase_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(usecase, field, value)

    # Recompute risk tier if relevant fields changed
    risk_fields = {"data_types", "data_residency", "external_sharing"}
    if risk_fields & set(update_data.keys()):
        usecase.risk_tier = compute_risk_tier(
            data_types=usecase.data_types,
            data_residency=usecase.data_residency,
            external_sharing=usecase.external_sharing,
        )

    db.commit()
    db.refresh(usecase)

    return usecase


@app.delete("/usecases/{usecase_id}", status_code=204)
def delete_usecase(usecase_id: int, db: Session = Depends(get_db)):
    """Delete a use case (legacy)."""
    usecase = db.query(UseCase).filter(UseCase.id == usecase_id).first()
    if usecase is None:
        raise HTTPException(status_code=404, detail="Use case not found")

    db.delete(usecase)
    db.commit()

    return None


# =============================================================================
# Intake Wizard HTML Routes
# =============================================================================

@app.get("/intake", response_class=HTMLResponse)
async def intake_list(request: Request, db: Session = Depends(get_db)):
    """List all intakes / start new intake page."""
    intakes = db.query(Intake).order_by(Intake.updated_at.desc()).all()
    return templates.TemplateResponse("intake/list.html", {
        "request": request,
        "intakes": intakes,
    })


@app.get("/intake/new")
async def intake_new(request: Request, db: Session = Depends(get_db)):
    """Create a new intake and redirect to step 1."""
    new_intake = Intake(
        system_name="",
        intake_status="draft",
        current_step=1,
        section_completion={},
    )
    db.add(new_intake)
    db.commit()
    db.refresh(new_intake)

    return RedirectResponse(url=f"/intake/{new_intake.id}/step/1", status_code=303)


@app.get("/intake/{intake_id}", response_class=HTMLResponse)
async def intake_view(intake_id: int, request: Request, db: Session = Depends(get_db)):
    """View intake - redirects to current step or review."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")

    if intake.intake_status == "submitted":
        return RedirectResponse(url=f"/intake/{intake_id}/report", status_code=303)

    return RedirectResponse(url=f"/intake/{intake_id}/step/{intake.current_step}", status_code=303)


@app.get("/intake/{intake_id}/step/{step_num}", response_class=HTMLResponse)
async def intake_step(
    intake_id: int,
    step_num: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Render a specific wizard step."""
    if step_num < 1 or step_num > 10:
        raise HTTPException(status_code=400, detail="Invalid step number")

    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")

    # Update current step
    intake.current_step = step_num
    db.commit()

    step_templates = {
        1: "intake/step_1_inventory.html",
        2: "intake/step_2_decision.html",
        3: "intake/step_3_data.html",
        4: "intake/step_4_ownership.html",
        5: "intake/step_5_regulatory.html",
        6: "intake/step_6_monitoring.html",
        7: "intake/step_7_risks.html",
        8: "intake/step_8_artifacts.html",
        9: "intake/step_9_readiness.html",
        10: "intake/step_10_actions.html",
    }

    return templates.TemplateResponse(step_templates[step_num], {
        "request": request,
        "intake": intake,
        "current_step": step_num,
        "total_steps": 10,
        "section_completion": compute_section_completion(intake),
    })


@app.get("/intake/{intake_id}/review", response_class=HTMLResponse)
async def intake_review(intake_id: int, request: Request, db: Session = Depends(get_db)):
    """Final review page before submission."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")

    return templates.TemplateResponse("intake/review.html", {
        "request": request,
        "intake": intake,
        "section_completion": compute_section_completion(intake),
    })


@app.get("/intake/{intake_id}/report", response_class=HTMLResponse)
async def intake_report_html(intake_id: int, request: Request, db: Session = Depends(get_db)):
    """View the readiness report."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")

    return templates.TemplateResponse("intake/report.html", {
        "request": request,
        "intake": intake,
    })


# =============================================================================
# Intake API Endpoints
# =============================================================================

@app.post("/api/intakes", response_model=IntakeResponse, status_code=201)
def create_intake(intake_data: IntakeCreate, db: Session = Depends(get_db)):
    """Create a new intake."""
    new_intake = Intake(
        system_name=intake_data.system_name,
        business_owner=intake_data.business_owner,
        business_owner_email=intake_data.business_owner_email,
        intake_status="draft",
        current_step=1,
        section_completion={},
    )

    db.add(new_intake)
    db.commit()
    db.refresh(new_intake)

    return new_intake


@app.get("/api/intakes", response_model=List[IntakeListItem])
def list_intakes(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all intakes with optional status filter."""
    query = db.query(Intake)

    if status:
        query = query.filter(Intake.intake_status == status)

    intakes = query.order_by(Intake.updated_at.desc()).offset(skip).limit(limit).all()
    return intakes


@app.get("/api/intakes/{intake_id}", response_model=IntakeResponse)
def get_intake(intake_id: int, db: Session = Depends(get_db)):
    """Get a specific intake with all related data."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")
    return intake


@app.patch("/api/intakes/{intake_id}")
def update_intake(
    intake_id: int,
    updates: IntakeSectionUpdate,
    db: Session = Depends(get_db),
):
    """Update intake (autosave endpoint)."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")

    # Apply section updates
    apply_section_updates(intake, updates)

    # Update completion tracking
    intake.section_completion = compute_section_completion(intake)
    intake.last_autosave_at = datetime.utcnow()

    db.commit()
    db.refresh(intake)

    return {"status": "saved", "last_saved": intake.last_autosave_at}


@app.post("/api/intakes/{intake_id}/submit")
def submit_intake(intake_id: int, db: Session = Depends(get_db)):
    """Submit intake for review."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")

    intake.intake_status = "submitted"
    intake.submitted_at = datetime.utcnow()

    db.commit()
    db.refresh(intake)

    return {"status": "submitted", "intake_id": intake.id}


@app.delete("/api/intakes/{intake_id}", status_code=204)
def delete_intake(intake_id: int, db: Session = Depends(get_db)):
    """Delete an intake."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")

    db.delete(intake)
    db.commit()

    return None


# =============================================================================
# Risk Assessment Sub-Resource Endpoints
# =============================================================================

@app.get("/api/intakes/{intake_id}/risks", response_model=List[RiskAssessmentResponse])
def list_risks(intake_id: int, db: Session = Depends(get_db)):
    """List all risk assessments for an intake."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")
    return intake.risk_assessments


@app.post("/api/intakes/{intake_id}/risks", response_model=RiskAssessmentResponse, status_code=201)
def create_risk(
    intake_id: int,
    risk_data: RiskAssessmentCreate,
    db: Session = Depends(get_db),
):
    """Add a risk assessment to an intake."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")

    new_risk = RiskAssessment(
        intake_id=intake_id,
        **risk_data.model_dump(),
    )

    db.add(new_risk)
    db.commit()
    db.refresh(new_risk)

    return new_risk


@app.patch("/api/intakes/{intake_id}/risks/{risk_id}", response_model=RiskAssessmentResponse)
def update_risk(
    intake_id: int,
    risk_id: int,
    risk_update: RiskAssessmentUpdate,
    db: Session = Depends(get_db),
):
    """Update a risk assessment."""
    risk = db.query(RiskAssessment).filter(
        RiskAssessment.id == risk_id,
        RiskAssessment.intake_id == intake_id,
    ).first()

    if risk is None:
        raise HTTPException(status_code=404, detail="Risk assessment not found")

    update_data = risk_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(risk, field, value)

    db.commit()
    db.refresh(risk)

    return risk


@app.delete("/api/intakes/{intake_id}/risks/{risk_id}", status_code=204)
def delete_risk(intake_id: int, risk_id: int, db: Session = Depends(get_db)):
    """Delete a risk assessment."""
    risk = db.query(RiskAssessment).filter(
        RiskAssessment.id == risk_id,
        RiskAssessment.intake_id == intake_id,
    ).first()

    if risk is None:
        raise HTTPException(status_code=404, detail="Risk assessment not found")

    db.delete(risk)
    db.commit()

    return None


# =============================================================================
# Required Artifact Sub-Resource Endpoints
# =============================================================================

@app.get("/api/intakes/{intake_id}/artifacts", response_model=List[RequiredArtifactResponse])
def list_artifacts(intake_id: int, db: Session = Depends(get_db)):
    """List all required artifacts for an intake."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")
    return intake.required_artifacts


@app.post("/api/intakes/{intake_id}/artifacts", response_model=RequiredArtifactResponse, status_code=201)
def create_artifact(
    intake_id: int,
    artifact_data: RequiredArtifactCreate,
    db: Session = Depends(get_db),
):
    """Add a required artifact to an intake."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")

    new_artifact = RequiredArtifact(
        intake_id=intake_id,
        **artifact_data.model_dump(),
    )

    db.add(new_artifact)
    db.commit()
    db.refresh(new_artifact)

    return new_artifact


@app.patch("/api/intakes/{intake_id}/artifacts/{artifact_id}", response_model=RequiredArtifactResponse)
def update_artifact(
    intake_id: int,
    artifact_id: int,
    artifact_update: RequiredArtifactUpdate,
    db: Session = Depends(get_db),
):
    """Update a required artifact."""
    artifact = db.query(RequiredArtifact).filter(
        RequiredArtifact.id == artifact_id,
        RequiredArtifact.intake_id == intake_id,
    ).first()

    if artifact is None:
        raise HTTPException(status_code=404, detail="Artifact not found")

    update_data = artifact_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(artifact, field, value)

    db.commit()
    db.refresh(artifact)

    return artifact


@app.delete("/api/intakes/{intake_id}/artifacts/{artifact_id}", status_code=204)
def delete_artifact(intake_id: int, artifact_id: int, db: Session = Depends(get_db)):
    """Delete a required artifact."""
    artifact = db.query(RequiredArtifact).filter(
        RequiredArtifact.id == artifact_id,
        RequiredArtifact.intake_id == intake_id,
    ).first()

    if artifact is None:
        raise HTTPException(status_code=404, detail="Artifact not found")

    db.delete(artifact)
    db.commit()

    return None


# =============================================================================
# Action Item Sub-Resource Endpoints
# =============================================================================

@app.get("/api/intakes/{intake_id}/actions", response_model=List[ActionItemResponse])
def list_actions(intake_id: int, db: Session = Depends(get_db)):
    """List all action items for an intake."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")
    return intake.action_items


@app.post("/api/intakes/{intake_id}/actions", response_model=ActionItemResponse, status_code=201)
def create_action(
    intake_id: int,
    action_data: ActionItemCreate,
    db: Session = Depends(get_db),
):
    """Add an action item to an intake."""
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    if intake is None:
        raise HTTPException(status_code=404, detail="Intake not found")

    new_action = ActionItem(
        intake_id=intake_id,
        **action_data.model_dump(),
    )

    db.add(new_action)
    db.commit()
    db.refresh(new_action)

    return new_action


@app.patch("/api/intakes/{intake_id}/actions/{action_id}", response_model=ActionItemResponse)
def update_action(
    intake_id: int,
    action_id: int,
    action_update: ActionItemUpdate,
    db: Session = Depends(get_db),
):
    """Update an action item."""
    action = db.query(ActionItem).filter(
        ActionItem.id == action_id,
        ActionItem.intake_id == intake_id,
    ).first()

    if action is None:
        raise HTTPException(status_code=404, detail="Action item not found")

    update_data = action_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(action, field, value)

    # Set completed timestamp if status changed to completed
    if action_update.status == "completed" and action.completed_at is None:
        action.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(action)

    return action


@app.delete("/api/intakes/{intake_id}/actions/{action_id}", status_code=204)
def delete_action(intake_id: int, action_id: int, db: Session = Depends(get_db)):
    """Delete an action item."""
    action = db.query(ActionItem).filter(
        ActionItem.id == action_id,
        ActionItem.intake_id == intake_id,
    ).first()

    if action is None:
        raise HTTPException(status_code=404, detail="Action item not found")

    db.delete(action)
    db.commit()

    return None
