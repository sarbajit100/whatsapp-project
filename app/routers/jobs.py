from fastapi import APIRouter, HTTPException, status

from app.utilities.models import JobResponse, JobStatus
from app.utilities.scheduler import cancel_job, get_job, list_jobs

router = APIRouter(prefix="/whatsapp/jobs", tags=["Jobs"])


@router.get("", response_model=list[JobResponse])
def get_all_jobs() -> list[JobResponse]:
    """List all scheduled jobs."""
    return list_jobs()


@router.get("/{job_id}", response_model=JobResponse)
def get_one_job(job_id: str) -> JobResponse:
    """Get the status of a specific scheduled job."""
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
def cancel(job_id: str) -> dict:
    """Cancel a pending scheduled job."""
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != JobStatus.pending:
        raise HTTPException(status_code=409, detail=f"Cannot cancel a job with status '{job.status}'")
    cancel_job(job_id)
    return {"job_id": job_id, "status": "cancelled"}
