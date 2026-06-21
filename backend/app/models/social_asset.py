from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class SocialAsset(TimestampMixin, Base):
    __tablename__ = "social_assets"
    __table_args__ = (UniqueConstraint("job_id", "platform", name="uq_job_platform"),)

    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"), index=True)
    platform: Mapped[str] = mapped_column(String(40))
    caption: Mapped[str] = mapped_column(Text)
    groups: Mapped[str] = mapped_column(Text, default="")
    visual_path: Mapped[str] = mapped_column(String(500), default="")

    job = relationship("Job", back_populates="social_assets")
