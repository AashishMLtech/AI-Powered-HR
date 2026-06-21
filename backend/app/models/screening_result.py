from sqlalchemy import Float, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ScreeningResult(TimestampMixin, Base):
    __tablename__ = "screening_results"

    application_id: Mapped[str] = mapped_column(ForeignKey("applications.id"), unique=True)
    cv_score: Mapped[float] = mapped_column(Float, default=0)
    github_score: Mapped[float] = mapped_column(Float, default=0)
    linkedin_score: Mapped[float] = mapped_column(Float, nullable=True)
    combined_score: Mapped[float] = mapped_column(Float, default=0)
    ai_resume_flag: Mapped[float] = mapped_column(Float, default=0)
    reasoning: Mapped[str] = mapped_column(Text, default="")
    details: Mapped[dict] = mapped_column(JSON, default=dict)

    application = relationship("Application", back_populates="screening_result")
