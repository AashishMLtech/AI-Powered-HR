from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hr_user import HRUser


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> HRUser | None:
        result = await self.db.execute(select(HRUser).where(HRUser.email == email))
        return result.scalar_one_or_none()

    async def create(self, email: str, full_name: str, password_hash: str) -> HRUser:
        user = HRUser(email=email, full_name=full_name, password_hash=password_hash)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
