from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: AsyncSession, model: type[ModelType]):
        self.db = db
        self.model = model

    async def add(self, item: ModelType) -> ModelType:
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete(self, item: ModelType) -> None:
        await self.db.delete(item)
        await self.db.commit()
