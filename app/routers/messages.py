from fastapi import APIRouter, HTTPException, status

from app.utilities.models import JobResponse, ScheduleRequest, SendNowRequest
from app.utilities.scheduler import schedule_message
from app.utilities.whatsapp import send_whatsapp_message

router = APIRouter(prefix="/whatsapp", tags=["Messages"])


@router.post("/send", status_code=status.HTTP_200_OK)
def send_now(payload: SendNowRequest) -> dict:
    """Send a WhatsApp message immediately."""
    try:
        sid = send_whatsapp_message(payload.to, payload.message)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return {"message_sid": sid, "status": "sent"}


@router.post("/schedule", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def schedule(payload: ScheduleRequest) -> JobResponse:
    """Schedule a WhatsApp message for a future time (or on a cron recurrence)."""
    return schedule_message(payload.to, payload.message, payload.send_at, payload.recurrence)
