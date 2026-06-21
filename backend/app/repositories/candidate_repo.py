from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate


class CandidateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert_by_email(
        self,
        full_name: str,
        email: str,
        phone: str,
        github_url: str,
        linkedin_url: str,
    ) -> Candidate:
        result = await self.db.execute(select(Candidate).where(Candidate.email == email))
        candidate = result.scalar_one_or_none()
        if candidate is None:
            candidate = Candidate(email=email, full_name=full_name)
            self.db.add(candidate)

        candidate.full_name = full_name
        candidate.phone = phone
        candidate.github_url = github_url
        candidate.linkedin_url = linkedin_url
        await self.db.commit()
        await self.db.refresh(candidate)
        return candidate

    async def get_by_id(self, candidate_id: str) -> Candidate | None:
        result = await self.db.execute(select(Candidate).where(Candidate.id == candidate_id))
        return result.scalar_one_or_none()
