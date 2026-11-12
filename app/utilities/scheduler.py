import logging
from datetime import datetime, timezone
from typing import Dict
from uuid import uuid4

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

from .models import JobStatus, JobResponse
from .whatsapp import send_whatsapp_message

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="UTC")

# In-memory job metadata store (replace with a DB for production)
_jobs: Dict[str, JobResponse] = {}


def _send_job(job_id: str, to: str, message: str) -> None:
    try:
        sid = send_whatsapp_message(to, message)
        logger.info("Sent message job_id=%s sid=%s", job_id, sid)
        if job_id in _jobs:
            _jobs[job_id].status = JobStatus.sent
    except Exception as exc:
        logger.error("Failed message job_id=%s error=%s", job_id, exc)
        if job_id in _jobs:
            _jobs[job_id].status = JobStatus.failed


def schedule_message(to: str, message: str, send_at: datetime, recurrence: str | None) -> JobResponse:
    job_id = str(uuid4())

    if recurrence:
        trigger = CronTrigger.from_crontab(recurrence, timezone="UTC")
    else:
        # Ensure the datetime is timezone-aware
        if send_at.tzinfo is None:
            send_at = send_at.replace(tzinfo=timezone.utc)
        trigger = DateTrigger(run_date=send_at)

    scheduler.add_job(
        _send_job,
        trigger=trigger,
        id=job_id,
        kwargs={"job_id": job_id, "to": to, "message": message},
        misfire_grace_time=60,
    )

    job = JobResponse(
        job_id=job_id,
        to=to,
        message=message,
        send_at=send_at,
        recurrence=recurrence,
        status=JobStatus.pending,
    )
    _jobs[job_id] = job
    return job


def cancel_job(job_id: str) -> bool:
    if job_id not in _jobs:
        return False
    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass  # job may have already fired
    _jobs[job_id].status = JobStatus.cancelled
    return True


def get_job(job_id: str) -> JobResponse | None:
    return _jobs.get(job_id)


def list_jobs() -> list[JobResponse]:
    return list(_jobs.values())
