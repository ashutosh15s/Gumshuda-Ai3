from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    org_type: str
    full_name: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str
    organization_id: str
    badge_or_id: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    organization_id: str
    is_active: bool

    class Config:
        from_attributes = True

class OrganizationCreate(BaseModel):
    name: str
    org_type: str
    state: str
    district: str

class OrganizationResponse(BaseModel):
    id: str
    name: str
    org_type: str
    state: str
    district: str

    class Config:
        from_attributes = True

class CaseCreate(BaseModel):
    person_name: str
    age: int
    gender: str
    missing_date: str
    district: str
    state: str
    fir_number: Optional[str] = None
    safe_summary: str
    guardian_contact: Optional[str] = None

class CaseResponse(BaseModel):
    id: str
    case_number: str
    person_name: str
    age: int
    gender: str
    missing_date: str
    district: str
    state: str
    fir_number: Optional[str] = None
    status: str
    safe_summary: str
    guardian_contact: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True