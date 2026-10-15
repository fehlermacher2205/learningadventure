from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from db.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column (Integer, primary_key=True, index= True)
    job_id = Column(String, index=True, unique= True)
    session_id = Column(String, index=True)
    status = Column(String )
    type = Column(String)
    result_id = Column(Integer, nullable= True)
    error = Column(String, nullable= True)
    created_at =  Column(DateTime(timezone=True), server_default=func.now())
    completed_at =  Column(DateTime(timezone=True), nullable=True)

    