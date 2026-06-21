from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.application import Application


class ApplicationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert(self, job_id: str, candidate_id: str, resume_path: str) -> Application:
        result = await self.db.execute(
            select(Application).where(
                Application.job_id == job_id,
                Application.candidate_id == candidate_id,
            )
        )
        application = result.scalar_one_or_none()
        if application is None:
            application = Application(job_id=job_id, candidate_id=candidate_id, consent_given=True, resume_path=resume_path)
            self.db.add(application)
        else:
            application.resume_path = resume_path
            application.status = "submitted"

        await self.db.commit()
        await self.db.refresh(application)
        return application

    async def list_for_job(self, job_id: str) -> list[Application]:
        result = await self.db.execute(
            select(Application)
            .options(selectinload(Application.candidate), selectinload(Application.screening_result))
            .where(Application.job_id == job_id)
        )
        return list(result.scalars().all())

    async def get_by_candidate_id(self, candidate_id: str) -> Application | None:
        result = await self.db.execute(
            select(Application)
            .options(selectinload(Application.candidate), selectinload(Application.screening_result))
            .where(Application.candidate_id == candidate_id)
        )
        return result.scalar_one_or_none()
