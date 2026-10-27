import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import MissingCase, User
from app.schemas import CaseResponse
from app.auth import get_current_user, require_role
from app.vector_store import add_case_vector, query_case_vectors

router = APIRouter(prefix="/api/cases", tags=["Missing Cases"])

@router.get("/", response_model=List[CaseResponse])
def list_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cases = db.query(MissingCase).all()
    sanitized = []
    for c in cases:
        case_data = CaseResponse.model_validate(c)
        if current_user.role not in ["POLICE_OFFICER", "ADMIN"]:
            case_data.guardian_contact = None
        sanitized.append(case_data)
    return sanitized

@router.post("/register", response_model=CaseResponse)
def register_case(
    person_name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    missing_date: str = Form(...),
    district: str = Form(...),
    state: str = Form(...),
    safe_summary: str = Form(...),
    fir_number: Optional[str] = Form(None),
    guardian_contact: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["POLICE_OFFICER", "ADMIN"]))
):
    case_ref = f"GUM-2026-{str(uuid.uuid4())[:6].upper()}"
    new_case = MissingCase(
        case_number=case_ref,
        person_name=person_name,
        age=age,
        gender=gender,
        missing_date=missing_date,
        district=district,
        state=state,
        fir_number=fir_number,
        safe_summary=safe_summary,
        guardian_contact=guardian_contact,
        organization_id=current_user.organization_id,
        created_by=current_user.id
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    doc_text = f"{person_name}, Age: {age}, Gender: {gender}, District: {district}, State: {state}. Summary: {safe_summary}"
    add_case_vector(
        case_id=new_case.id,
        document_text=doc_text,
        metadata={
            "case_number": case_ref,
            "district": district,
            "state": state,
            "age": age,
            "gender": gender
        }
    )

    return new_case

@router.get("/search-rag")
def search_cases_rag(query: str, current_user: User = Depends(get_current_user)):
    results = query_case_vectors(query_text=query, n_results=5)
    return {"query": query, "matches": results}