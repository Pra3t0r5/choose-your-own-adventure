# Sqlalchemy 1.0 ---------------------------
# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.sql import func
#
# from db.database import Base
#
#
# class StoryJob(Base):
#   __tablename__ = "story_jobs"
#
#   id = Column(Integer, primary_key=True, index=True)
#   job_id = Column(String, index=True, unique=True)
#   session_id = Column(String, index=True)
#   theme = Column(String)
#   status = Column(String)
#   story_id = Column(Integer, nullable=True)
#   error = Column(String, nullable=True)
#   created_at = Column(DateTime(timezone=True), default=func.now())
#   completed_at = Column(DateTime(timezone=True), nullable=True)
#
# Sqlalchemy 2.0 ---------------------------
from db.database import Base

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class StoryJob(Base):
    __tablename__ = "story_jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_id: Mapped[str] = mapped_column(index=True, unique=True)
    session_id: Mapped[str] = mapped_column(index=True)
    theme: Mapped[str]
    status: Mapped[str]
    story_id: Mapped[int | None] = mapped_column(nullable=True)
    error: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
