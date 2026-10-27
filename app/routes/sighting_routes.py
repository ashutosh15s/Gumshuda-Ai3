from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional
from app.models import User
from app.auth import get_current_user
from app.vector_store import query_case_vectors

router = APIRouter(prefix="/api/sightings", tags=["Sightings"])

@router.post("/submit")
def submit_sighting(
    observed_date: str = Form(...),
    state: str = Form(...),
    district: str = Form(...),
    context_notes: str = Form(...),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user)
):
    query_string = f"Observed in {district}, {state}. Notes: {context_notes}"
    results = query_case_vectors(query_text=query_string, n_results=3)

    return {
        "status": "RECORDED_PENDING_REVIEW",
        "observed_date": observed_date,
        "location": f"{district}, {state}",
        "context": context_notes,
        "potential_case_leads": results
    }