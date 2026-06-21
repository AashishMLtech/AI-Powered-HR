from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.database import get_db
from app.models.hr_user import HRUser
from app.schemas.application import CandidateListItem, LinkedInCheckRequest
from app.services.candidate_service import CandidateService


router = APIRouter(tags=["candidates"])


@router.get("/jobs/{job_id}/candidates", response_model=list[CandidateListItem])
async def list_candidates(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    _ = user
    return await CandidateService(db).list_candidates_for_job(job_id)


@router.get("/candidates/{candidate_id}/screening")
async def get_screening(
    candidate_id: str,
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    _ = user
    return await CandidateService(db).get_screening(candidate_id)


@router.patch("/candidates/{candidate_id}/linkedin-check")
async def update_linkedin_score(
    candidate_id: str,
    payload: LinkedInCheckRequest,
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    _ = user
    return await CandidateService(db).update_linkedin_score(candidate_id, payload.linkedin_score, payload.notes)
