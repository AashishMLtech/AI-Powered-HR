from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.application import ApplicationResponse
from app.services.candidate_service import CandidateService


router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationResponse)
async def submit_application(
    job_id: str = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    github_url: str = Form(""),
    linkedin_url: str = Form(""),
    consent_given: bool = Form(...),
    resume: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    return await CandidateService(db).submit_application(
        job_id=job_id,
        full_name=full_name,
        email=email,
        phone=phone,
        github_url=github_url,
        linkedin_url=linkedin_url,
        consent_given=consent_given,
        resume=resume,
    )
