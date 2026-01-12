"""FastAPI application for AI Use-Case Registry."""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import engine, get_db, Base
from app.models import UseCase
from app.schemas import UseCaseCreate, UseCaseUpdate, UseCaseResponse
from app.risk import compute_risk_tier

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Use-Case Registry",
    description="A beginner-friendly registry for tracking AI use cases",
    version="1.0.0",
)

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Serve the executive dashboard page."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    """Serve the use case registration form."""
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics for the executive view."""
    # Get all use cases
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
    }


@app.post("/usecases", response_model=UseCaseResponse, status_code=201)
def create_usecase(usecase: UseCaseCreate, db: Session = Depends(get_db)):
    """Create a new use case."""
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
    """List all use cases with pagination."""
    usecases = db.query(UseCase).offset(skip).limit(limit).all()
    return usecases


@app.get("/usecases/{usecase_id}", response_model=UseCaseResponse)
def get_usecase(usecase_id: int, db: Session = Depends(get_db)):
    """Get a specific use case by ID."""
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
    """Update a use case (partial update)."""
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
    """Delete a use case."""
    usecase = db.query(UseCase).filter(UseCase.id == usecase_id).first()
    if usecase is None:
        raise HTTPException(status_code=404, detail="Use case not found")

    db.delete(usecase)
    db.commit()

    return None
