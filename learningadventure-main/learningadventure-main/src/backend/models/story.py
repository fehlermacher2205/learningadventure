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
import uuid
from db.database import Base
# they should belong to a sub folder
# this is for convenience 

class StoryTextHistory(Base):
    __tablename__ = "text_history"
    __table_args__ = (
        UniqueConstraint("story_id", "position_in_story","version"),
    )
    story_id = Column(String, ForeignKey("stories.id"),nullable=False, primary_key= True)
    position_in_story = Column(Integer,default =1 , nullable=False,  primary_key= True)
    version =  Column(Integer, default = 1,nullable=False, primary_key= True)
    choice_text = Column(String, nullable=False)  
    content = Column (String, nullable=False, default ="")  


class Story(Base):
    __tablename__ = "stories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column (String,default="New Story")
    background = Column(String, default="")
    background_ver = Column(Integer,default = 1)
    background_version_count = Column(Integer,default = 1)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    created_at =  Column(DateTime(timezone=True), server_default=func.now())
    profile_id = Column(String, ForeignKey("profile.id"),nullable=False)
    page_count = Column(Integer, default=-1)  
    answers_snapshot = Column(JSON, nullable=False, default=list)
    active_goal_profile = relationship(
            "ActiveGoalsInProfile",
            back_populates="active_story",
            uselist=False 
    )
    is_active = Column(Boolean, default=True, nullable=False)
    pages = relationship(
        "StoryPage",
        back_populates="story", 
        cascade="all, delete-orphan",
        foreign_keys="StoryPage.story_id",
        order_by="StoryPage.page_number"
    )
    actions = relationship(
        "Action",
        back_populates="story",
        cascade="all, delete-orphan"
    )
    profile = relationship(
        "Profile",
        back_populates="stories",
        uselist=False,
    )


class StoryPage(Base): 
    __tablename__ = "story_pages"
    __table_args__ = (
        UniqueConstraint("story_id", "page_number"),
    )
#page = db.query(StoryPage).filter(
#    StoryPage.story_id == story_id,
#    StoryPage.page_number == 5
#).first()
    id = Column(Integer, primary_key=True)
    page_number = Column(Integer, nullable = False)
    page_ver = Column(Integer,default = 1)
    page_version_count = Column(Integer,default = 1)
    story_id = Column(String, ForeignKey("stories.id"), nullable=False)
    choice_text = Column(String, nullable=False)  
    content = Column (String)
    story = relationship(
        "Story",
        back_populates="pages",
        foreign_keys="StoryPage.story_id"
    )
    

