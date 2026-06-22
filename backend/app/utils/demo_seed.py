from app.database import AsyncSessionLocal, create_db_tables
from app.repositories.user_repo import UserRepository
from app.utils.security import hash_password


async def seed_hr_user() -> None:
    await create_db_tables()
    async with AsyncSessionLocal() as db:
        repo = UserRepository(db)
        existing = await repo.get_by_email("hr@example.com")
        if existing:
            existing.full_name = "HR Admin"
            existing.password_hash = hash_password("password123")
            await db.commit()
            await db.refresh(existing)
            return

        await repo.create(
            email="hr@example.com",
            full_name="HR Admin",
            password_hash=hash_password("password123"),
        )
