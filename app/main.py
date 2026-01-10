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
async def index(request: Request):
    """Serve the HTML form page."""
    return templates.TemplateResponse("index.html", {"request": request})


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
