from typing import Optional
from datetime import datetime
from pydantic import BaseModel
# removed 

class JobBase(BaseModel):
    type: str
class JobCreate(JobBase):
    pass 
class JobResponse(JobBase):
    session_id: str
    job_id:str
    status:str
    created_at: datetime
    result_id : Optional[int] = None
    completed_at : Optional[datetime] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True

