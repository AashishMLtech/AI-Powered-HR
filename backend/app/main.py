import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.database import create_db_tables
from app.utils.demo_seed import seed_hr_user


app = FastAPI(title="AI HR Automation Platform")

allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://ai-powered-hr.vercel.app",
]

extra_origins = os.getenv("CORS_ORIGINS", "")
for origin in [item.strip() for item in extra_origins.split(",") if item.strip()]:
    allowed_origins.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    await create_db_tables()
    await seed_hr_user()


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/v1")
