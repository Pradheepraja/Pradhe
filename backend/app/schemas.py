from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class StudySessionCreate(BaseModel):
    work_minutes: int = 25
    break_minutes: int = 5


class StudySessionOut(BaseModel):
    id: int
    start_time: datetime
    end_time: Optional[datetime]
    work_minutes: int
    break_minutes: int
    focus_score: Optional[float]

    class Config:
        from_attributes = True


class DistractionCreate(BaseModel):
    type: str
    session_id: Optional[int] = None
    duration_sec: Optional[int] = None
    emotion: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class DistractionOut(BaseModel):
    id: int
    type: str
    timestamp: datetime
    duration_sec: Optional[int]
    emotion: Optional[str]
    details: Optional[Dict[str, Any]]
    session_id: Optional[int]

    class Config:
        from_attributes = True


class DailyStat(BaseModel):
    date: str
    focus_score: float
    total_distractions: int
    idle_minutes: int
    emotion_counts: Dict[str, int]


class Suggestion(BaseModel):
    message: str


class AIAnalysisRequest(BaseModel):
    image_base64: Optional[str] = None
    log_event: bool = True
    session_id: Optional[int] = None


class AIAnalysisResponse(BaseModel):
    attention: bool
    emotion: Optional[str]
    confidence: Optional[float]
    is_distracted: bool
    nudges: List[str] = []
