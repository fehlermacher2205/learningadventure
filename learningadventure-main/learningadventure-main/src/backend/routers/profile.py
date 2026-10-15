import uuid
from typing import List, Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from nanoid import generate
from sqlalchemy.orm import Session

from core.exceptions import (
    InvalidSessionError,
    ObjectNotFoundError,
    PermissionDeniedError,
)
from db.database import get_db
from models.profile import (
    MAX_QUESTION_NUM,
    BackgroundQuestion,
    Profile,
    ProfilePrompt,
    ProfileStatus,
    PredefinedGoal
)
from models.story import Story
from models.user import User
from models.goal_action import Goal,Action,ActiveGoalsInProfile
from schemas.profile import (
    CreateProfileRequest,
    ProfileResponse,
    PromptUpdateRequest,
    PromptsResponse,
    QuestionBase,
    RecentStoryResponse,
    QuestionResponse,
    AddNewQuestionRequest,
    BaseProfile,
    ChangeVisibilityRequest,
    ActiveProfileResponse
)
from schemas.story import StoryResponse,EditBackgroundRequest
from schemas.common import MessageResponse
from schemas.goal import (
    GoalTemplateResponse,
    CreateTemplateGoalRequest,
    RemoveTemplateGoalRequest,
    EditTemplateGoalRequest,
    GoalResponse, 
    GoalResponse,
    AddGoalToActiveGoalsRequest,
    GoalBase,
    GenerateGoalsRequest,
    ChangeActiveGoalPriorityRequest,
    AddPredefinedGoalToActiveGoalsRequest,
    RemoveGoalFromActiveGoalsRequest
)

from services.goals_services import generate_goals,check_duplicate
from services.user_profile import (
    get_current_user,
    validateOwnership,
    does_question_exist,
    get_draft_profile
)
from services.utility import save_to_db
from services.validate_service import validate_id,validate_string_id
from services.user_profile import check_profile_visibility_for_user
from services.story_service import createDefaultStory
router = APIRouter(
    prefix="/profiles",
    tags=["profile"]
)


#@router.get("/get_selected_profile_no_cookie", response_model = ShortProfileResponse)
#def get_selected_profile_for_story_endpoint(
#    profile = Depends(get_profile_with_token_id_without_cookie),
#):
#    return ShortProfileResponse(
#        profile_name=profile.profile_name,
#        profile_id=profile.profile_id
#    )
# this one is not open for public use
# 

# user would still need an account to use the system tho


    
@router.get("/{profile_id}", response_model = ProfileResponse)
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = validate_string_id(db, "profile", profile_id, "id")
    return profile




# user will have to call this first before they can
# get active story

# consider packing them into the services package to preserve business's logic
@router.get("/{profile_id}/my_activeProfile", response_model=ActiveProfileResponse)
def get_me_activeGoals(
    profile_id: str,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    goals_profile = db.query(ActiveGoalsInProfile).filter(
        ActiveGoalsInProfile.profile_id == profile.id, 
        ActiveGoalsInProfile.user_id == user.id
    ).first()
    
    if goals_profile is None:
        check_profile_visibility_for_user(profile=profile,user=user)
        answers_snapshot = []
        for question in profile.questions:
            answers_snapshot.append((question.question_text, ""))
        
        new_story = createDefaultStory(
            profile=profile,
            user=user,
            db=db,
            answers_snapshot= answers_snapshot
            )

        goals_profile = ActiveGoalsInProfile(
            user_id=user.id,
            profile_id=profile.id,
            active_story_id = new_story.id

        )
        save_to_db(db,goals_profile)

    return goals_profile


@router.post("/{profile_id}/my_add_all", response_model=ActiveProfileResponse)
def add_all_goal_endpoint(
    profile_id: str,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    goals_profile = db.query(ActiveGoalsInProfile).filter(
        ActiveGoalsInProfile.profile_id == profile.id, 
        ActiveGoalsInProfile.user_id == user.id
    ).first()
    
    if goals_profile is None:
        raise ObjectNotFoundError(" Active goals-Object not found!")
        
    active_goals = goals_profile.goals
    
    for goal in profile.predefined_goals:
        new_goal = Goal(
            title = goal.title,
            category = goal.category,
            level = goal.level,
            skill = goal.skill,
            active_profile_id = goals_profile.id,
            predefinedgoal_id = goal.id # <-- ADD THIS LINE
        )
        check_duplicate(goals = active_goals, new_goal = new_goal)
        active_goals.append(new_goal)
        
    db.commit()
    db.refresh(goals_profile)
    return goals_profile




@router.get("/{profile_id}/get_active_story", response_model=RecentStoryResponse)
def get_active_stories_endpoint(
    profile_id: str,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    
    # 1. Fetch the single active story for this profile/user
    recent_story = db.query(Story).filter(
        Story.profile_id == profile.id,
        Story.user_id == user.id,
        Story.is_active == True
    ).order_by(Story.created_at.desc()).first()
    
    # 2. If no active story exists, create a new one
    if not recent_story:
        # Check for the newest inactive story to inherit the answers_snapshot
        latest_inactive_story = db.query(Story).filter(
            Story.profile_id == profile.id,
            Story.user_id == user.id,
            Story.is_active == False
        ).order_by(Story.created_at.desc()).first()
        
        # Inherit snapshot if the story exists, else default to an empty list
        if latest_inactive_story and latest_inactive_story.answers_snapshot:
            answers_snapshot = latest_inactive_story.answers_snapshot
        else:
            answers_snapshot = []
            
        new_story = createDefaultStory(
            profile=profile,
            user=user,
            db=db,
            answers_snapshot=answers_snapshot
        )
        
        return new_story
        
    return recent_story

@router.get("/{profile_id}/get_expire_stories", response_model = List[RecentStoryResponse])
def get_expire_stories_endpoint(
    profile_id: str,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    profile = validate_string_id(db, "profile", profile_id, "id")
    user = get_current_user(user_session_token, db)
    stories = db.query(Story).filter(
        Story.profile_id == profile.id,
        Story.user_id ==user.id,
        Story.is_active == False
    ).order_by(Story.created_at.desc()).all()
# need to set profile_id in the session response model
    return stories






    


@router.post("/{profile_id}/add_question", response_model=ProfileResponse)
def add_new_question_to_profile(
    profile_id: str,
    request: AddNewQuestionRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    validateOwnership(user = user, profile = profile)
    questions = profile.questions
    if len(questions) >= MAX_QUESTION_NUM:
        raise PermissionDeniedError(f"Cannot add more than {MAX_QUESTION_NUM} questions")
    new_question = BackgroundQuestion(
        question_text=request.question_text,
        position=len(questions) + 1,
        profile_id=profile.id  
    )
    profile.questions.append(new_question)
    db.commit()
    db.refresh(profile)
    return profile 






######################################3
######################################
######################################

######################################
######################################
######################################
# likely that it is removed the below shits 





@router.post("/{profile_id}/create_predefined_goal", response_model = List[GoalTemplateResponse])
def create_predefined_goal_endpoint(
    profile_id: str,
    request: CreateTemplateGoalRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    profile = validate_string_id(db, "profile", profile_id, "id")
    user = get_current_user(user_session_token, db)
    validateOwnership(user = user, profile = profile)
    new_goal = PredefinedGoal(
        title = request.title,
        category = request.category,
        skill = request.skill,
        level = request.level,
        profile_id = profile.id,
        position_in_profile = len(profile.predefined_goals) + 1
    )
    profile.predefined_goals.append(new_goal)
    db.commit()
    db.refresh(profile)
    return profile.predefined_goals

@router.put("/{profile_id}/editbackground", response_model = ProfileResponse)
def edit_profile_template_background_story_endpoint(
    profile_id : str,
    request: EditBackgroundRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    profile = validate_string_id(db, "profile", profile_id, "id")
    user = get_current_user(user_session_token, db)
    validateOwnership(user = user, profile = profile)
    profile.predefined_background = request.background
    db.commit()
    return profile

@router.put("/{profile_id}/edit_predefined_goal", response_model = List[GoalTemplateResponse])
def edit_predefined_goal_endpoint(
    profile_id: str,
    request: EditTemplateGoalRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    profile = validate_string_id(db, "profile", profile_id, "id")
    user = get_current_user(user_session_token, db)
    validateOwnership(user = user, profile = profile)
    if (request.position_in_profile - 1) >= len(profile.predefined_goals):
        raise ObjectNotFoundError("Predefined goal not found") 
    goal_to_edit = profile.predefined_goals[request.position_in_profile - 1]
    if not goal_to_edit:
        raise ObjectNotFoundError("Predefined goal not found")
    
    if request.title is not None:
        goal_to_edit.title = request.title
    if request.category is not None:
        goal_to_edit.category = request.category
    if request.skill is not None:
        goal_to_edit.skill = request.skill
    if request.level is not None:
        goal_to_edit.level = request.level

    db.commit()
    db.refresh(profile)
    return profile.predefined_goals





# goals session here









@router.post("/{profile_id}/my_removegoal", response_model=List[GoalResponse])
def remove_goal_fromactivegoals(
    profile_id: str,
    request: RemoveGoalFromActiveGoalsRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    active_goals = db.query(ActiveGoalsInProfile).filter(ActiveGoalsInProfile.profile_id == profile.id,ActiveGoalsInProfile.user_id == user.id).first()
    if active_goals is None:
        raise ObjectNotFoundError(" User does not have Active Goals for target profile!")
    target_goal = None
    for goal in active_goals.goals:
        if goal.predefinedgoal_id == request.goal_id:
            target_goal = goal
            break

    if target_goal is None:
        raise ObjectNotFoundError("Target goal does not exist")

    db.delete(target_goal)
    db.commit()

    updated_goals = db.query(Goal).filter(
        Goal.active_profile_id == active_goals.id
    ).all()

    return updated_goals

@router.put("/{profile_id}/my_changegoalPriority", response_model= List[GoalResponse])
def change_goal_priority_in_myactivegoals(
    profile_id: str,
    request: ChangeActiveGoalPriorityRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    active_goals = db.query(ActiveGoalsInProfile).filter(ActiveGoalsInProfile.profile_id == profile.id,ActiveGoalsInProfile.user_id == user.id).first()
    if active_goals is None:
        raise ObjectNotFoundError(" User does not have Active Goals for target profile!")
    target_goal = None
    for goal in active_goals.goals:
        if goal.predefinedgoal_id == request.goal_id:
            target_goal = goal
            break
    if target_goal is None:
        raise ObjectNotFoundError("Target goal does not exist!")
    target_goal.is_focused = not target_goal.is_focused
    db.commit()
    db.flush()
    return active_goals.goals

@router.post("/{profile_id}/my_addgoal_predefined", response_model= List[GoalResponse])
def add_predefined_goal_to_myactivegoals(
    profile_id: str,
    request: AddPredefinedGoalToActiveGoalsRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    active_goals = db.query(ActiveGoalsInProfile).filter(ActiveGoalsInProfile.profile_id == profile.id,ActiveGoalsInProfile.user_id == user.id).first()
    if active_goals is None:
        active_goals = ActiveGoalsInProfile(
            profile_id = profile.id,
            user_id = user.id
        )
    predefinedgoal = db.query(PredefinedGoal).filter(PredefinedGoal.id == request.predefinedgoal_id).first()
    if predefinedgoal is None:
        raise ObjectNotFoundError(" Predefined goal not found!")
    
    goal = Goal(
        title= predefinedgoal.title,
        category= predefinedgoal.category,
        skill= predefinedgoal.skill,
        level= predefinedgoal.level,
        skill_score= 0,
        active_profile_id= active_goals.id,
        predefinedgoal_id = predefinedgoal.id
    )
    active_goals.goals.append(goal)
    save_to_db(db, active_goals)
    return active_goals.goals




@router.delete("/{profile_id}/remove_predefined_goal", response_model= List[GoalTemplateResponse])
def remove_predefined_goal_from_profile(
    profile_id: str,
    request: RemoveTemplateGoalRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    validateOwnership(user = user, profile = profile)
    goal_to_remove = profile.predefined_goals[request.position_in_profile - 1]
    if not goal_to_remove:
        raise ObjectNotFoundError("Predefined goal not found")
    
    for g in profile.predefined_goals:
        if g.position_in_profile > goal_to_remove.position_in_profile:
            g.position_in_profile -= 1
    profile.predefined_goals.remove(goal_to_remove)
    
    db.commit()
    db.refresh(profile)
    return profile.predefined_goals
@router.post("/{profile_id}/my_addgoal", response_model= List[GoalResponse])
def add_goal_to_myactivegoals(
    profile_id: str,
    request: AddGoalToActiveGoalsRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    active_goals = db.query(ActiveGoalsInProfile).filter(ActiveGoalsInProfile.profile_id == profile.id,ActiveGoalsInProfile.user_id == user.id).first()
    if active_goals is None:
        active_goals = ActiveGoalsInProfile(
            profile_id = profile.id,
            user_id = user.id
        )
    goal = Goal(
        title= request.title,
        category= request.category,
        skill= request.skill,
        level= request.level,
        skill_score= 0,
        active_profile_id= active_goals.id
    )
    active_goals.goals.append(goal)
    save_to_db(db, active_goals)
    return active_goals.goals
@router.put("/{profile_id}/edit_prompts",response_model=PromptsResponse)
def edit_profile_prompts_endpoint(
    request: PromptUpdateRequest,
    user_session_token: str = Cookie(None),
    profile_id: str = None,
    
    db: Session = Depends(get_db),
):  
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    validateOwnership(user = user, profile = profile)
    if not profile.prompt:
        raise ObjectNotFoundError("Critical Error: Profile prompts not found")
    
    # Update the specific prompt based on its type
    if request.prompt_type == "quest_prompt":
        profile.prompt.quest_prompt = request.new_prompt
    elif request.prompt_type == "page_prompt":
        profile.prompt.page_prompt = request.new_prompt
    elif request.prompt_type == "goal_prompt":
        profile.prompt.goal_prompt = request.new_prompt
    elif request.prompt_type == "action_prompt":
        profile.prompt.action_prompt = request.new_prompt
    else:
        raise ObjectNotFoundError(f"Invalid prompt type: {request.prompt_type}")
    db.commit()
    return profile.prompt


@router.get("/{profile_id}/getname", response_model = ProfileResponse)
def get_profile_name_endpoint(
    profile_id: str, 
    db: Session = Depends(get_db)
    ):
    profile = validate_string_id(db, "profile", profile_id, "id")
    return profile
# editname
@router.put("/{profile_id}/editname", response_model=ProfileResponse)
def edit_profile_name_endpoint(
    request: BaseProfile,
    user_session_token: str = Cookie(None),
    profile_id: str = None,
    db: Session = Depends(get_db),
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    validateOwnership(user = user, profile = profile)
    profile.profile_name = request.profile_name
    db.commit()
    return profile
@router.put("/{profile_id}/change_visibility", response_model=ProfileResponse)
def change_profile_visibility(
    profile_id: str,
    request: ChangeVisibilityRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", profile_id, "id")
    validateOwnership(user = user, profile = profile)
    profile.visible = request.visible
    db.commit()
    db.refresh(profile)
    return profile

