import uuid 
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from db.database import get_db
from models.job import Job
from schemas.job import JobResponse
from services.validate_service import validate_type_and_id
router = APIRouter(
    prefix ="/jobs",
    tags=["jobs"]
)

@router.get("/{job_id}", response_model =JobResponse)
def get_job_status_by_job_id(job_id: str, db: Session = Depends(get_db)):

    job = db.query(Job).filter(Job.job_id == job_id).first()

    if not job:
        raise HTTPException(status_code = 404, detail = "Job not found")
    
    return job
@router.get("/jobs/internal/{id}")
def get_job_status_by_index(id: str, db: Session = Depends(get_db)):
    job = validate_type_and_id(db, "job", id)
    return job