from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hr_user import HRUser
from app.models.job import Job
from app.repositories.job_repo import JobRepository
from app.repositories.social_asset_repo import SocialAssetRepository
from app.schemas.job import JobCreate, JobUpdate
from app.services.jd_service import rewrite_jd
from app.services.social_service import generate_social_assets


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = JobRepository(db)

    async def create_job(self, payload: JobCreate, user: HRUser) -> Job:
        ai_jd = await rewrite_jd(payload.raw_jd, payload.title)
        job = Job(
            title=payload.title,
            department=payload.department,
            location=payload.location,
            raw_jd=payload.raw_jd,
            ai_jd=ai_jd,
            status="pending_review",
            created_by_id=user.id,
        )
        return await self.repo.create(job)

    async def list_jobs(self) -> list[Job]:
        return await self.repo.list_all()

    async def get_job(self, job_id: str) -> Job:
        job = await self.repo.get_by_id(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="JOB_NOT_FOUND")
        return job

    async def update_job(self, job_id: str, payload: JobUpdate) -> Job:
        job = await self.get_job(job_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(job, key, value)
        return await self.repo.update(job)

    async def approve_jd(self, job_id: str) -> Job:
        job = await self.get_job(job_id)
        job.status = "published"
        saved = await self.repo.update(job)
        await generate_social_assets(saved, SocialAssetRepository(self.db))
        return saved

    async def reject_jd(self, job_id: str) -> Job:
        job = await self.get_job(job_id)
        job.status = "rejected"
        return await self.repo.update(job)

    async def regenerate_jd(self, job_id: str) -> Job:
        job = await self.get_job(job_id)
        job.ai_jd = await rewrite_jd(job.raw_jd, job.title)
        job.status = "pending_review"
        return await self.repo.update(job)
