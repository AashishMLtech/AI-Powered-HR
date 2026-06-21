from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Candidate(TimestampMixin, Base):
    __tablename__ = "candidates"

    full_name: Mapped[str] = mapped_column(String(140))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(40), default="")
    github_url: Mapped[str] = mapped_column(String(255), default="")
    linkedin_url: Mapped[str] = mapped_column(String(255), default="")

    applications = relationship("Application", back_populates="candidate")
