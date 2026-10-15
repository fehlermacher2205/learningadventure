from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    Boolean, 
    ForeignKey, 
    JSON,
    UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
import uuid
from db.database import Base
class ActiveGoalsInProfile(Base):
    __tablename__ = "activegoalsprofile"
    id = Column(Integer, primary_key=True)
    __table_args__ = (
        UniqueConstraint('profile_id', 'user_id'),
    )
    profile_id = Column(
        String, 
        ForeignKey("profile.id"),
        nullable= False
    )
    active_story_id = Column(
        String, 
        ForeignKey("stories.id"),
        nullable=False
    )
    active_story = relationship(
            "Story", 
            back_populates="active_goal_profile"
    )

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) 
    # back_populates matches the variable name "active_profile" in the Goal class
    goals = relationship(
        "Goal",
        back_populates="active_profile"
    )
    user = relationship("User", back_populates="active_profiles")
    profile = relationship("Profile")
    #last_use = Column(DateTime(timezone=True), server_default=func.now())
# we will add a 


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)
    skill = Column(String)
    level = Column(String)
    created_at =  Column(DateTime(timezone=True), server_default=func.now())
    skill_score = Column(Integer, default=0)
    priority = Column(Integer, default=0)
    predefinedgoal_id = Column(Integer, ForeignKey("predefined_goals.id"), nullable=True)
    is_focused = Column(Boolean, default=False, nullable=False)
    active_profile_id = Column(Integer, ForeignKey("activegoalsprofile.id"))
    active_profile = relationship(
            "ActiveGoalsInProfile",
            back_populates="goals"
        )
    

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    action = Column(String)
    title = Column(String)
    value = Column(Integer)
    reasoning = Column(String)
    category = Column(String)
    skill = Column(String)
    created_at =  Column(DateTime(timezone=True), server_default=func.now())
    story_page_id = Column(Integer, ForeignKey("story_pages.id", ondelete="CASCADE"), index=True)
    story_id = Column(String, ForeignKey("stories.id", ondelete="CASCADE"), index=True,nullable=False)

    story = relationship(
        "Story",
        back_populates="actions"
)