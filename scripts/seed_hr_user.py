import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(ROOT))

from app.utils.demo_seed import seed_hr_user


async def main() -> None:
    await seed_hr_user()
    print("HR user ready: hr@example.com / password123")


if __name__ == "__main__":
    asyncio.run(main())
