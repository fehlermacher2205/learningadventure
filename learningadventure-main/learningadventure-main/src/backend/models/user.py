from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    matriculation_number = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    language = Column(String, default = "en", nullable= False)
    is_admin = Column(Boolean, default=False, nullable=False)
    # 1-to-many relationship
    # user can have multiple profiles, but each profile belongs to one user
# owned profiles
    profiles = relationship(
        "Profile", 
        back_populates="user",
        foreign_keys="[Profile.user_id]",
        cascade="all, delete-orphan"
    )
    active_profiles = relationship(
        "ActiveGoalsInProfile", 
        back_populates="user",
        cascade="all, delete-orphan" # If user is deleted, delete their progress
    )

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True)  # token
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now(), index=True)
    last_interaction = Column(DateTime, server_default=func.now(), onupdate=func.now())