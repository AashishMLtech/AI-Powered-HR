from app.ai.client_factory import get_llm_client
from app.models.job import Job
from app.models.social_asset import SocialAsset
from app.repositories.social_asset_repo import SocialAssetRepository


PLATFORMS = ["linkedin", "twitter", "facebook", "instagram"]


async def generate_social_assets(job: Job, repo: SocialAssetRepository) -> list[SocialAsset]:
    client = get_llm_client()
    assets: list[SocialAsset] = []

    for platform in PLATFORMS:
        caption = await client.social_caption(platform, job.title, job.ai_jd)
        if platform == "twitter":
            caption = caption[:280]
        assets.append(
            SocialAsset(
                job_id=job.id,
                platform=platform,
                caption=caption,
                groups="AI-suggested, unverified: HR Jobs, Startup Hiring, Local Careers",
                visual_path="",
            )
        )

    return await repo.upsert_many(assets)
