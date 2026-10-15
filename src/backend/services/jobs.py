from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from models.job import Job
from services.action_services import evaluate_last_action
TASK_REGISTRY = {
    "evaluate_last_action": evaluate_last_action,
#    "goal_generation": generate_goal_task,
# The idea is dropped because we require user input 
# to select the goal and the processing time is also low
}

# This function will simply just add job to the database
# it does not care about the type of the job or the validity of the input
def create_job(
    db: Session,
    background_tasks: BackgroundTasks,
    session_id: str,
    theme: str,
    type: str,
    profile_id:int 
) -> Job:
    job_id = str(uuid.uuid4())

    job = Job(
        job_id=job_id,
        session_id=session_id,
        type=type,
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    generate_task = TASK_REGISTRY.get(type)
    if generate_task:
        background_tasks.add_task(
            generate_task,
            job_id,
            theme,
            session_id,
            profile_id
        )
    return job

def update_job(db: Session, job: Job, status: str, error: str = None, result_id: int = None):
    job.status = status
    job.completed_at = datetime.now()
    if error:
        job.error = error

    if result_id:
        job.result_id = result_id

    db.commit()

from db.database import SessionLocal
from services.story_service import generate_story
def generate_story_task(job_id: str, content: str, session_id: str, profile_id: int):
    db = SessionLocal()
    job = None
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise ValueError(f"Job not found: {job_id}")

        update_job(db, job, "processing")

        story_list = generate_story(db, session_id, content, profile_id)
        update_job(
            db,
            job,
            "completed",
            result_id=story_list
        )

    except Exception as e:
        if job:
            update_job(db, job, "failed", error=str(e))

    finally:
        db.close()

