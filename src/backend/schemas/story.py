from typing import List,Optional, Dict, Tuple
from pydantic import BaseModel, Field , ConfigDict
from schemas.action import ActionResponse
from schemas.goal import GoalResponse
# its just bad name
# page is an option of the story
class EditBackgroundRequest(BaseModel):
    background: str
class GenerateStoryRequest(BaseModel):
    choice_text: str

class CreateStoryPageRequest(BaseModel):
    choice_text: str

class StoryPageResponse(BaseModel):
    story_id: str
    choice_text: str
    content: str
    page_number: int
    model_config = ConfigDict(from_attributes=True)





# read and write use the same one
class StoryQuestionsSnapshot(BaseModel):
    answers_snapshot: List[Tuple[str, str]] = Field(
        default_factory= list
    )
    
    model_config = ConfigDict(from_attributes=True)
class StoryResponse(BaseModel):
    id: str
    title: str
    background: str
    page_count: int
    pages: List[StoryPageResponse]
    actions: List[ActionResponse]
    answers_snapshot: List[Tuple[str, str]]
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
    
