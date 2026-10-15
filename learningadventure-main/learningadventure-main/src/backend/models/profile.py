from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base
from sqlalchemy.types import JSON
from nanoid import generate
from enum import Enum, IntEnum  
MAX_QUESTION_NUM = 10


class ProfileStatus(IntEnum):
    draft = -1
    private = 0
    link_only = 1
    public = 2

class PredefinedGoal(Base):
    __tablename__ = "predefined_goals"
    id = Column(Integer, primary_key=True, index=True,nullable=False)  # Position of the goal in the list
    title = Column(String, nullable=False, default="")
    category = Column(String, nullable=False, default="")
    skill = Column(String, nullable=False, default="")
    level = Column(String, nullable=False, default="")
    profile_id = Column(String, ForeignKey("profile.id", ondelete="CASCADE"), nullable=False)
    position_in_profile = Column(Integer, nullable=False)  # Position of the goal in the profile's predefined goals list
    profile = relationship(
        "Profile",
        back_populates="predefined_goals"
    )
# keep it simple for noew
    #next_goal_id = Column(Integer, ForeignKey("predefined_goals.id"), nullable=True)  # Self-referential foreign key
    #next_goal = relationship("PredefinedGoal", remote_side=[id])  # Relationship to itself

class ProfilePrompt(Base):
    __tablename__ = "ProfilePrompt"
    id = Column(Integer, primary_key=True)
    profile_id = Column(String, ForeignKey("profile.id"))
    quest_prompt = Column(String, nullable=False, default="")
    page_prompt = Column(String, nullable=False, default="")
    goal_prompt = Column(String, nullable=False, default="")
    action_prompt = Column(String, nullable=False, default="")
    profile = relationship(
        "Profile",
        back_populates="prompt"
    )

class BackgroundQuestion(Base):
    __tablename__ = "BackgroundQuestion"
    id = Column(Integer, primary_key=True)
    profile_id = Column(String, ForeignKey("profile.id"))
    question_text = Column(String, nullable=False, default="")
    position = Column(Integer, nullable=False, index=True, default=MAX_QUESTION_NUM)  # New field to track the order of questions
    profile = relationship(
        "Profile",
        back_populates="questions"
    )

class Profile(Base):
    __tablename__ = "profile"
    # please notice that profile session id is shorter than chat/story session id
    # frontend will request a profile using profile token
#server use id to return response
    id = Column(String, primary_key=True, default=lambda: str(generate(size=12) ))
    
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
#client use session id to request response



    # non unique, cant be null, update on delete
# please note that user_id here means the owner
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) 

    profile_name = Column(String, nullable=False,default="Unnamed Profile")
    visible = Column(Integer, default=ProfileStatus.public)  # -1: unset, 0: private, 1: link-only, 2: public
    predefined_background = Column (String, nullable= False, default="No background defined!")
    prompt = relationship(
        "ProfilePrompt",
        back_populates="profile",
        cascade="all, delete-orphan",
        uselist=False
    )

        # Relationships
    # This tells SQLAlchemy to automatically load a list of Goal objects
    # and attach it to the Python property named profile or ".goals"
    user = relationship(
        "User", 
        back_populates="profiles",
        foreign_keys=[user_id]
    )
    questions = relationship(
        "BackgroundQuestion",
        back_populates="profile",
        cascade="all, delete-orphan",
        order_by="BackgroundQuestion.position"
    )
    stories = relationship(
        "Story",
        back_populates="profile"
    )
    predefined_goals = relationship(
        "PredefinedGoal",
        back_populates="profile",
        cascade="all, delete-orphan"
    )
# router
# add Predefinedgoal to profile
# 
