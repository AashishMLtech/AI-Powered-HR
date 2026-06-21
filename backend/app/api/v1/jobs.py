from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.database import get_db
from app.models.hr_user import HRUser
from app.repositories.social_asset_repo import SocialAssetRepository
from app.schemas.job import JobCreate, JobResponse, JobUpdate, PublicJobResponse
from app.schemas.social_asset import SocialAssetResponse
from app.services.job_service import JobService


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobResponse)
async def create_job(
    payload: JobCreate,
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    return await JobService(db).create_job(payload, user)


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    _ = user
    return await JobService(db).list_jobs()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    _ = user
    return await JobService(db).get_job(job_id)


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    payload: JobUpdate,
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    _ = user
    return await JobService(db).update_job(job_id, payload)


@router.patch("/{job_id}/approve", response_model=JobResponse)
async def approve_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    _ = user
    return await JobService(db).approve_jd(job_id)


@router.patch("/{job_id}/reject", response_model=JobResponse)
async def reject_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    _ = user
    return await JobService(db).reject_jd(job_id)


@router.post("/{job_id}/regenerate", response_model=JobResponse)
async def regenerate_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    _ = user
    return await JobService(db).regenerate_jd(job_id)


@router.get("/{job_id}/public", response_model=PublicJobResponse)
async def get_public_job(job_id: str, db: AsyncSession = Depends(get_db)):
    job = await JobService(db).get_job(job_id)
    if job.status != "published":
        raise HTTPException(status_code=404, detail="PUBLIC_JOB_NOT_FOUND")
    return job


@router.get("/{job_id}/social-assets", response_model=list[SocialAssetResponse])
async def get_social_assets(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    user: HRUser = Depends(get_current_user),
):
    _ = user
    return await SocialAssetRepository(db).list_for_job(job_id)
