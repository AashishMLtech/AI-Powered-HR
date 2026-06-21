from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.models.application import Application
from app.repositories.application_repo import ApplicationRepository
from app.repositories.candidate_repo import CandidateRepository
from app.repositories.job_repo import JobRepository
from app.repositories.screening_result_repo import ScreeningResultRepository
from app.services.screening_service import screen_application
from app.utils.file_validator import validate_resume_file


class CandidateService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings = get_settings()

    async def submit_application(
        self,
        job_id: str,
        full_name: str,
        email: str,
        phone: str,
        github_url: str,
        linkedin_url: str,
        consent_given: bool,
        resume: UploadFile,
    ) -> Application:
        if not consent_given:
            raise HTTPException(status_code=400, detail="CONSENT_REQUIRED")

        job = await JobRepository(self.db).get_by_id(job_id)
        if job is None or job.status != "published":
            raise HTTPException(status_code=404, detail="PUBLIC_JOB_NOT_FOUND")

        content = await validate_resume_file(resume, self.settings.max_file_size_mb)
        candidate = await CandidateRepository(self.db).upsert_by_email(
            full_name=full_name,
            email=email,
            phone=phone,
            github_url=github_url,
            linkedin_url=linkedin_url,
        )

        upload_dir = Path(self.settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)
        safe_name = f"{job_id}_{candidate.id}_{resume.filename}".replace("/", "_").replace("\\", "_")
        resume_path = upload_dir / safe_name
        resume_path.write_bytes(content)

        app_repo = ApplicationRepository(self.db)
        application = await app_repo.upsert(job_id=job_id, candidate_id=candidate.id, resume_path=str(resume_path))

        result = await self.db.execute(
            select(Application)
            .options(selectinload(Application.candidate), selectinload(Application.job))
            .where(Application.id == application.id)
        )
        loaded_application = result.scalar_one()
        resume_text = content.decode("utf-8", errors="ignore")
        await screen_application(loaded_application, resume_text, ScreeningResultRepository(self.db))
        return application

    async def list_candidates_for_job(self, job_id: str) -> list[dict]:
        applications = await ApplicationRepository(self.db).list_for_job(job_id)
        rows = []
        for application in applications:
            candidate = application.candidate
            result = application.screening_result
            rows.append(
                {
                    "candidate_id": candidate.id,
                    "application_id": application.id,
                    "full_name": candidate.full_name,
                    "email": candidate.email,
                    "github_url": candidate.github_url,
                    "linkedin_url": candidate.linkedin_url,
                    "combined_score": result.combined_score if result else 0,
                    "cv_score": result.cv_score if result else 0,
                    "github_score": result.github_score if result else 0,
                    "linkedin_score": result.linkedin_score if result else None,
                    "ai_resume_flag": result.ai_resume_flag if result else 0,
                    "status": application.status,
                }
            )
        return sorted(rows, key=lambda item: item["combined_score"], reverse=True)

    async def get_screening(self, candidate_id: str) -> dict:
        application = await ApplicationRepository(self.db).get_by_candidate_id(candidate_id)
        if application is None or application.screening_result is None:
            raise HTTPException(status_code=404, detail="SCREENING_NOT_FOUND")
        candidate = application.candidate
        screening = application.screening_result
        return {
            "candidate": {
                "id": candidate.id,
                "full_name": candidate.full_name,
                "email": candidate.email,
                "github_url": candidate.github_url,
                "linkedin_url": candidate.linkedin_url,
            },
            "application": {
                "id": application.id,
                "job_id": application.job_id,
                "status": application.status,
            },
            "screening": {
                "cv_score": screening.cv_score,
                "github_score": screening.github_score,
                "linkedin_score": screening.linkedin_score,
                "combined_score": screening.combined_score,
                "ai_resume_flag": screening.ai_resume_flag,
                "reasoning": screening.reasoning,
                "details": screening.details,
            },
        }

    async def update_linkedin_score(self, candidate_id: str, linkedin_score: float, notes: str) -> dict:
        data = await self.get_screening(candidate_id)
        result = data["screening"]
        application = await ApplicationRepository(self.db).get_by_candidate_id(candidate_id)
        if application is None or application.screening_result is None:
            raise HTTPException(status_code=404, detail="SCREENING_NOT_FOUND")
        result = application.screening_result
        result.linkedin_score = linkedin_score
        from app.services.scoring_service import compute_combined_score

        result.combined_score = compute_combined_score(result.cv_score, result.github_score, linkedin_score)
        result.details = {**(result.details or {}), "linkedin_notes": notes}
        await ScreeningResultRepository(self.db).update(result)
        return await self.get_screening(candidate_id)
