from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings


settings = get_settings()
engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def create_db_tables() -> None:
    from app.models.base import Base
    from app.models import application, candidate, hr_user, job, screening_result, social_asset

    _ = (application, candidate, hr_user, job, screening_result, social_asset)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
