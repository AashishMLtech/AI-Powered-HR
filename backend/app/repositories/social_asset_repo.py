from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.social_asset import SocialAsset


class SocialAssetRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert_many(self, assets: list[SocialAsset]) -> list[SocialAsset]:
        saved: list[SocialAsset] = []
        for asset in assets:
            result = await self.db.execute(
                select(SocialAsset).where(
                    SocialAsset.job_id == asset.job_id,
                    SocialAsset.platform == asset.platform,
                )
            )
            existing = result.scalar_one_or_none()
            if existing:
                existing.caption = asset.caption
                existing.groups = asset.groups
                existing.visual_path = asset.visual_path
                saved.append(existing)
            else:
                self.db.add(asset)
                saved.append(asset)

        await self.db.commit()
        for item in saved:
            await self.db.refresh(item)
        return saved

    async def list_for_job(self, job_id: str) -> list[SocialAsset]:
        result = await self.db.execute(select(SocialAsset).where(SocialAsset.job_id == job_id))
        return list(result.scalars().all())
