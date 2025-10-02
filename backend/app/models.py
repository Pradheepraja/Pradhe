from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
    UniqueConstraint,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    streak_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    focus_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    sessions: Mapped[list[StudySession]] = relationship("StudySession", back_populates="user")
    distractions: Mapped[list[DistractionEvent]] = relationship("DistractionEvent", back_populates="user")
    badges: Mapped[list[UserBadge]] = relationship("UserBadge", back_populates="user")


class StudySession(Base):
    __tablename__ = "study_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    work_minutes: Mapped[int] = mapped_column(Integer, default=25, nullable=False)
    break_minutes: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    focus_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    user: Mapped[User] = relationship("User", back_populates="sessions")
    distractions: Mapped[list[DistractionEvent]] = relationship("DistractionEvent", back_populates="session")


class DistractionEvent(Base):
    __tablename__ = "distraction_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    session_id: Mapped[Optional[int]] = mapped_column(ForeignKey("study_sessions.id"), nullable=True)

    # "idle", "tab", "emotion"
    type: Mapped[str] = mapped_column(String(32), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    duration_sec: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    emotion: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    user: Mapped[User] = relationship("User", back_populates="distractions")
    session: Mapped[Optional[StudySession]] = relationship("StudySession", back_populates="distractions")


class Badge(Base):
    __tablename__ = "badges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(255))
    emoji: Mapped[str] = mapped_column(String(8))

    __table_args__ = (UniqueConstraint("key", name="uq_badge_key"),)


class UserBadge(Base):
    __tablename__ = "user_badges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    badge_id: Mapped[int] = mapped_column(ForeignKey("badges.id"), index=True)
    awarded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="badges")
    badge: Mapped[Badge] = relationship("Badge")
