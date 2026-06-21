from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Job(TimestampMixin, Base):
    __tablename__ = "jobs"

    title: Mapped[str] = mapped_column(String(180), index=True)
    department: Mapped[str] = mapped_column(String(120), default="")
    location: Mapped[str] = mapped_column(String(120), default="")
    raw_jd: Mapped[str] = mapped_column(Text)
    ai_jd: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(40), default="pending_review", index=True)
    created_by_id: Mapped[str] = mapped_column(ForeignKey("hr_users.id"))

    created_by = relationship("HRUser")
    applications = relationship("Application", back_populates="job")
    social_assets = relationship("SocialAsset", back_populates="job")
