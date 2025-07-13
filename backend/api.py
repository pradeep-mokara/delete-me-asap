from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Job
from .db import SessionLocal
from .scheduler import enqueue_job

router = APIRouter()


class JobPayload(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    target: str
    priority: int = 0
    max_retries: int = 0


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/jobs/submit")
def submit_job(payload: JobPayload, db: Session = Depends(get_db)):
    job = Job(**payload.dict())
    db.add(job)
    db.commit()
    db.refresh(job)

    enqueue_job(job)
    return {"job_id": str(job.id)}


@router.get("/jobs/{job_id}/status")
def get_job_status(job_id: UUID, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": job.status}


@router.get("/health")
def health_check():
    return {"status": "ok"}
