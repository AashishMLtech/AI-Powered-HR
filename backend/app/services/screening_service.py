from app.ai.client_factory import get_llm_client
from app.models.application import Application
from app.models.screening_result import ScreeningResult
from app.repositories.screening_result_repo import ScreeningResultRepository
from app.services.scoring_service import compute_combined_score
from app.utils.github_client import get_public_github_summary


async def screen_application(application: Application, resume_text: str, repo: ScreeningResultRepository) -> ScreeningResult:
    client = get_llm_client()
    candidate = application.candidate
    job = application.job

    cv = await client.score_cv(resume_text, job.title, job.ai_jd)
    github_summary = await get_public_github_summary(candidate.github_url)
    github = await client.assess_github(github_summary, job.title)
    ai_flag = await client.ai_resume_flag(resume_text)

    combined = compute_combined_score(cv["score"], github["score"])
    result = ScreeningResult(
        application_id=application.id,
        cv_score=cv["score"],
        github_score=github["score"],
        linkedin_score=None,
        combined_score=combined,
        ai_resume_flag=ai_flag["score"],
        reasoning=f"CV: {cv['reasoning']} GitHub: {github['reasoning']}",
        details={
            "github": github_summary,
            "ai_flag_reasoning": ai_flag["reasoning"],
            "advisory": True,
        },
    )
    return await repo.upsert(result)
