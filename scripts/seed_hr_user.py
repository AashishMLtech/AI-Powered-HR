import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(ROOT))

from app.database import AsyncSessionLocal, create_db_tables
from app.repositories.user_repo import UserRepository
from app.utils.security import hash_password


async def main() -> None:
    await create_db_tables()
    async with AsyncSessionLocal() as db:
        repo = UserRepository(db)
        existing = await repo.get_by_email("hr@example.com")
        if existing:
            existing.full_name = "HR Admin"
            existing.password_hash = hash_password("password123")
            await db.commit()
            await db.refresh(existing)
            print("HR user already exists: hr@example.com")
            return
        await repo.create(
            email="hr@example.com",
            full_name="HR Admin",
            password_hash=hash_password("password123"),
        )
        print("Created HR user: hr@example.com / password123")


if __name__ == "__main__":
    asyncio.run(main())
