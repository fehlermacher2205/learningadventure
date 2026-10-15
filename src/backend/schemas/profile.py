from typing import List,Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field,ConfigDict

from schemas.goal import GoalResponse
from models.profile import ProfileStatus


class PromptsResponse(BaseModel):
    quest_prompt: Optional[str] = None
    page_prompt: Optional[str] = None
    goal_prompt: Optional[str] = None
    action_prompt: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
class PromptUpdateRequest(BaseModel):
    new_prompt: str
    prompt_type: str # "quest", "page", "goal", "action"




class QuestionBase(BaseModel):
    question_text: str
    position: int
class QuestionResponse(QuestionBase):

    model_config = ConfigDict(from_attributes=True)


# its use for add, remove and edit
class QuestionEditRequest(QuestionBase):
    pass


class BaseProfile(BaseModel):
    profile_name: str

class CreateProfileRequest(BaseProfile):
    visible: ProfileStatus = ProfileStatus.draft


class ShortProfileResponse(BaseProfile):
    profile_id: str = Field(validation_alias="id")
    model_config = ConfigDict(from_attributes=True)

class RecentStoryResponse(BaseModel):
    story_id: str = Field(validation_alias="id")
    profile_id: str
    title: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class PredefinedGoalResponse(BaseModel):
    id :int
    title: str
    category:str
    skill: str
    level: str
    position_in_profile:int
    class Config:
        from_attributes= True
class ProfileResponse(BaseProfile):
    profile_id: str = Field(validation_alias="id")
    updated_at: datetime
    questions: List[QuestionResponse] = Field(default_factory=list)
    predefined_goals: List[PredefinedGoalResponse] = Field(default_factory=list)
    user_id : int
    prompt : PromptsResponse  
    visible: ProfileStatus
    predefined_background: str = ""
    model_config = ConfigDict(from_attributes=True)

class QuestionBase(BaseModel):
    question_text: str
    position: int


class AddNewQuestionRequest(BaseModel):
    question_text: str

class ChangeVisibilityRequest(BaseModel):
    visible: ProfileStatus

class AddActiveProfileRequest(BaseModel):
    profile_id: str

class ActiveProfileResponse(BaseModel):
    id: int
    profile_id: str 
    goals: List[GoalResponse]
    active_story_id: str
    model_config = ConfigDict(from_attributes=True)
