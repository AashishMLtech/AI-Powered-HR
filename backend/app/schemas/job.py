from datetime import datetime
from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    department: str = ""
    location: str = ""
    raw_jd: str


class JobUpdate(BaseModel):
    title: str | None = None
    department: str | None = None
    location: str | None = None
    ai_jd: str | None = None


class JobResponse(BaseModel):
    id: str
    title: str
    department: str
    location: str
    raw_jd: str
    ai_jd: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PublicJobResponse(BaseModel):
    id: str
    title: str
    department: str
    location: str
    ai_jd: str

    model_config = {"from_attributes": True}
