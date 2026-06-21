from datetime import datetime
from pydantic import BaseModel, EmailStr


class ApplicationResponse(BaseModel):
    id: str
    job_id: str
    candidate_id: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CandidateListItem(BaseModel):
    candidate_id: str
    application_id: str
    full_name: str
    email: EmailStr
    github_url: str
    linkedin_url: str
    combined_score: float
    cv_score: float
    github_score: float
    linkedin_score: float | None
    ai_resume_flag: float
    status: str


class LinkedInCheckRequest(BaseModel):
    linkedin_score: float
    notes: str = ""
