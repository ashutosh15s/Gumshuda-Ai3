from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Organization, User, MissingCase
from app.schemas import OrganizationCreate, OrganizationResponse
from app.auth import require_role

router = APIRouter(prefix="/api/admin", tags=["Police & System Admin"])

@router.post("/organizations", response_model=OrganizationResponse)
def create_organization(
    org: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["ADMIN"]))
):
    existing = db.query(Organization).filter(Organization.name == org.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organization already registered")

    new_org = Organization(
        name=org.name,
        org_type=org.org_type,
        state=org.state,
        district=org.district
    )
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

@router.get("/organizations", response_model=List[OrganizationResponse])
def get_organizations(db: Session = Depends(get_db)):
    return db.query(Organization).all()

@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["ADMIN", "POLICE_OFFICER"]))
):
    total_cases = db.query(MissingCase).count()
    active_cases = db.query(MissingCase).filter(MissingCase.status == "OPEN").count()
    total_orgs = db.query(Organization).count()
    return {
        "total_cases": total_cases,
        "active_cases": active_cases,
        "total_verified_organizations": total_orgs
    }