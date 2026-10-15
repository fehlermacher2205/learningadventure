from typing import List,Optional, Dict
from datetime import datetime

from pydantic import BaseModel ,Field, ConfigDict

class GoalTemplateResponse(BaseModel):
    predefined_goal_id: int =Field(validation_alias="id")
    title: str
    category: str
    skill: str
    level: str 
    profile_id: str
    position_in_profile: int
    model_config = ConfigDict(from_attributes=True)

class CreateTemplateGoalRequest(BaseModel):
    title: str
    category: str
    skill: str
    level: str
class EditTemplateGoalRequest(BaseModel):
    position_in_profile: int
    title: Optional[str] = None
    category: Optional[str] = None
    skill: Optional[str] = None
    level: Optional[str] = None
class RemoveTemplateGoalRequest(BaseModel):
    position_in_profile: int


class GoalBase(BaseModel):
    title: str
    category: str
    skill: str
    level: str
class AddGoalToActiveGoalsRequest(GoalBase):
    pass
class RemoveGoalFromActiveGoalsRequest(BaseModel):
    goal_id:int
class AddPredefinedGoalToActiveGoalsRequest(BaseModel):
    predefinedgoal_id : int
class GenerateGoalsRequest(GoalBase):
    context: str
class ChangeActiveGoalPriorityRequest(BaseModel):
    goal_id: int # it is the id of the predefined goal in the profile. not the id of the active goal

class GoalResponse(GoalBase):
    goal_id: int = Field(validation_alias="id")
    is_focused: bool 
    created_at: datetime
    skill_score: int
    priority: int
    predefinedgoal_id:int
    model_config = ConfigDict(from_attributes=True)


