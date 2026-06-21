from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.screening_result import ScreeningResult


class ScreeningResultRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert(self, result_data: ScreeningResult) -> ScreeningResult:
        result = await self.db.execute(
            select(ScreeningResult).where(ScreeningResult.application_id == result_data.application_id)
        )
        existing = result.scalar_one_or_none()
        if existing is None:
            self.db.add(result_data)
            await self.db.commit()
            await self.db.refresh(result_data)
            return result_data

        existing.cv_score = result_data.cv_score
        existing.github_score = result_data.github_score
        existing.linkedin_score = result_data.linkedin_score
        existing.combined_score = result_data.combined_score
        existing.ai_resume_flag = result_data.ai_resume_flag
        existing.reasoning = result_data.reasoning
        existing.details = result_data.details
        await self.db.commit()
        await self.db.refresh(existing)
        return existing

    async def update(self, result: ScreeningResult) -> ScreeningResult:
        await self.db.commit()
        await self.db.refresh(result)
        return result
