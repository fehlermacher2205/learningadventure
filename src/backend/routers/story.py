from fastapi import APIRouter, Depends, Response, Cookie
from sqlalchemy.orm import Session
from db.database import get_db
from services.story_service import (
    generate_story_page,
)
from core.exceptions import ObjectNotFoundError, PermissionDeniedError, InvalidSessionError
from schemas.goal import GoalResponse,GoalBase,GenerateGoalsRequest

from services.goals_services import generate_goals

from uuid import uuid4
from services.utility import (
    save_to_db
)
from schemas.action import ActionResponse
from services.action_services import evaluate_last_action
from services.validate_service import (
    validate_id,
    check_story_ownership,
    validate_string_id
)
from services.user_profile import get_current_user
from services.story_service import generate_story
from schemas.story import (
    StoryResponse, 
    StoryPageResponse, 
    CreateStoryPageRequest,
    GenerateStoryRequest,
    EditBackgroundRequest,
    StoryQuestionsSnapshot
)
from schemas.action import (
    ActionResponse
)
from typing import List, Tuple

from models.goal_action import Goal,ActiveGoalsInProfile
router = APIRouter(
    prefix = "/stories",
    tags= ["stories"]
)


@router.get("/{story_id}", response_model = StoryResponse)
def get_full_story_endpoint(
    story_id: str,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
    )-> StoryResponse:
    user = get_current_user(user_session_token, db)
    story = check_story_ownership(user, story_id= story_id, db=db)
    return story
@router.put("/{story_id}/endstory", response_model = str)
def endstory_endpoint(
    story_id: str,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
    )-> StoryResponse:
    user = get_current_user(user_session_token, db)
    story = check_story_ownership(user, story_id= story_id, db=db)
    story.is_active = False
    db.commit()
    return "success"

@router.post("/{story_id}/generatepage", response_model = StoryPageResponse)
def generate_story_page_endpoint(
    request: CreateStoryPageRequest,
    story_id: str,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    story = check_story_ownership(user, story_id= story_id, db=db)
    goals_profile = db.query(ActiveGoalsInProfile).filter(
        ActiveGoalsInProfile.profile_id == story.profile_id, 
        ActiveGoalsInProfile.user_id == user.id
    ).first()
    if goals_profile is None:
        raise ObjectNotFoundError("Does not exist a goals profile for submitted story_id")
    new_page = generate_story_page(
        db = db, 
        story=story, 
        choice_text=request.choice_text,
        goals = goals_profile.goals
        )
    return new_page



@router.get("/{story_id}/pages/{page_number}", response_model=StoryPageResponse)
def get_story_page_end_point(
    story_id: str,
    page_number: int,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
) -> StoryPageResponse:

    user = get_current_user(user_session_token, db)
    story = check_story_ownership(user, story_id= story_id, db=db)
    page = story.pages[page_number - 1] 
    if page is None:
        raise ObjectNotFoundError(f"Page number {page_number} not found in story with id {story_id}.")
    return page

@router.post("/{story_id}/generategoals", response_model=List[GoalResponse])
def generate_goals_for_story_endpoint(
    story_id: str,
    request: GenerateGoalsRequest,
    
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    story = check_story_ownership(user, story_id= story_id, db=db)
    #goals = profile.goals
    newgoals = generate_goals( context=request.context, story=story)
    return [
        GoalResponse(
            title=goal.title,
            category=goal.category,
            skill=goal.skill,
            level=goal.level,
            skill_score= 0
        )
        for goal in newgoals
    ]










@router.get("/{story_id}/action_history", response_model=List[ActionResponse])
def get_action_history_endpoint(
    story_id: str,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):  
    user = get_current_user(user_session_token, db)
    story = check_story_ownership(user, story_id= story_id, db=db)
    actions =story.actions
    return actions




@router.post("/{story_id}/action_evaluation",response_model=List[ActionResponse])
def last_action_evaluation_endpoint(
    story_id: str,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    story = check_story_ownership(user, story_id= story_id, db=db)
    return evaluate_last_action(story = story, db = db,user = user)








@router.put("/{story_id}/editsnapshot", response_model= List[Tuple[str, str]])
def edit_questions_snapshot_endpoint(
    story_id : str,
    request: StoryQuestionsSnapshot,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    story = check_story_ownership(user, story_id= story_id, db=db)
    snapshot_tuple = request.answers_snapshot
    story.answers_snapshot= snapshot_tuple
    story.page_count = 0
    db.commit()
    db.refresh(story)
    return story.answers_snapshot

@router.put("/{story_id}/editbackground", response_model = StoryResponse)
def edit_background_story_endpoint(
    story_id : str,
    request: EditBackgroundRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    story = check_story_ownership(user, story_id= story_id, db=db)
    story.background = request.background
    db.commit()
    return story


@router.post ("/{story_id}/generatebackground", response_model = StoryResponse)
def generate_background_story(
    story_id: str,
    request: GenerateStoryRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):

    user = get_current_user(user_session_token, db)
    story = check_story_ownership(user, story_id= story_id, db=db)
    goals_profile = db.query(ActiveGoalsInProfile).filter(
        ActiveGoalsInProfile.profile_id == story.profile_id, 
        ActiveGoalsInProfile.user_id == user.id
    ).first()
    if goals_profile is None:
        raise ObjectNotFoundError("Does not exist a goals profile for submitted story_id")
    pages = story.pages
    for page in pages:
        if page.content:
            db.delete(page)
    story.page_count = 0
# create story
    story = generate_story(choice_text=request.choice_text,story=story,db=db, goals = goals_profile.goals)

    return story





# WARNING:


# This endpoint is old structure created for background
# task that took way too long to run in the frontend


# NOTE:
# If you want to know how it a story is generated
# please check out the story generation task in services/story_builder.py
#@router.post("/create",response_model=JobResponse)
#def create_story_using_background_task(
#    request: CreateStoryRequest,
#    background_tasks: BackgroundTasks,
#    response: Response,
#    story_id : str = Depends(get_story_id),
#    db: Session = Depends(get_db)
#) -> Job:
#    response.set_cookie(key= "story_id", value = story_id, httponly= True)
#    job = create_job(
#        db ,
#        background_tasks,
#        story_id,
#        request.content,
#        "story_generation",
#        request.profile_id
#    )
#    return job




