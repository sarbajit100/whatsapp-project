from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator
import re


class JobStatus(str, Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"
    cancelled = "cancelled"


class ScheduleRequest(BaseModel):
    to: str                        # e.g. "whatsapp:+919876543210"
    message: str
    send_at: datetime              # ISO-8601, timezone-aware recommended
    recurrence: Optional[str] = None  # cron expression, e.g. "0 9 * * 1-5"

    @field_validator("to")
    @classmethod
    def validate_to(cls, v: str) -> str:
        if not v.startswith("whatsapp:+"):
            raise ValueError("'to' must start with 'whatsapp:+' followed by digits")
        digits = v[len("whatsapp:+"):]
        if not re.fullmatch(r"\d{7,15}", digits):
            raise ValueError("Phone number must be 7–15 digits after the country code")
        return v

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("message cannot be empty")
        if len(v) > 4096:
            raise ValueError("message exceeds 4096 characters")
        return v


class JobResponse(BaseModel):
    job_id: str
    to: str
    message: str
    send_at: datetime
    recurrence: Optional[str]
    status: JobStatus


class SendNowRequest(BaseModel):
    to: str
    message: str

    @field_validator("to")
    @classmethod
    def validate_to(cls, v: str) -> str:
        if not v.startswith("whatsapp:+"):
            raise ValueError("'to' must start with 'whatsapp:+' followed by digits")
        return v
