from fastapi import APIRouter, Depends, Cookie
from httpcore import request
from db.database import get_db
from schemas.user import UserCreateRequest, UserPageResponse
from sqlalchemy.orm import Session
from services.validate_service import validate_id
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.user import User
from fastapi import Response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import (
    User
)

from models.user import UserSession
from uuid import uuid4
from schemas.user import UserPageResponse,UserLoginResponse
from services.user_profile import (
    get_current_user,
    create_user_session_login_token,
    get_draft_profile
)
from schemas.user import RegisterRequest, LoginRequest



from services.utility import save_to_db
from schemas.profile import ProfileResponse, CreateProfileRequest,AddActiveProfileRequest,ActiveProfileResponse
from models.profile import Profile, ProfilePrompt, ProfileStatus
from models.goal_action import ActiveGoalsInProfile
from typing import List

from core.exceptions import ObjectNotFoundError, PermissionDeniedError, InvalidSessionError
from services.validate_service import validate_string_id
from services.user_profile import check_profile_visibility_for_user
router = APIRouter(
    prefix ="/user",
    tags=["user"]
)
# model is base class from schema 
# the pydantic class that we use to validate and 
# serialize data for API requests and responses



# minimal for now
@router.post("/register",response_model =  UserPageResponse)
def register(
    request: RegisterRequest, 
    db: Session = Depends(get_db)
):
    try:
        user = User(
            matriculation_number=request.matriculation_number,
            username=request.username,
            password=request.password
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="User with this matriculation number already exists."
        )

@router.post("/login",response_model =  UserLoginResponse)
def login(
    request: LoginRequest,
    response: Response, 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.matriculation_number == request.matriculation_number).first()

    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_user_session_login_token()

    session = UserSession(
        id=token,
        user_id=user.id
    )

    db.add(session)
    db.commit()

    response.set_cookie(
        key="user_session_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return UserLoginResponse(
        username=user.username,
        matriculation_number=user.matriculation_number,
        token=token
    )

@router.get("/get_user", response_model = UserPageResponse)
def get_user(
    db: Session = Depends(get_db),
    user_session_token: str = Cookie(None)
):
    user = get_current_user(user_session_token, db)
    return user

# Logout endpoint to clear the user session cookie
@router.post("/logout")
def logout(
    response: Response
):
    response.delete_cookie(key="user_session_token")
    return {"message": "Logged out successfully"}















@router.post("/addactiveprofile", response_model=ActiveProfileResponse)
def add_active_profile_endpoint(
    request : AddActiveProfileRequest,
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    profile = validate_string_id(db, "profile", request.profile_id, "id")
    check_profile_visibility_for_user(profile=profile, user=user)
    goals_profile = db.query(ActiveGoalsInProfile).filter(ActiveGoalsInProfile.profile_id == profile.id, ActiveGoalsInProfile.user_id ==user.id).first()
    if goals_profile is None:
        goals_profile = ActiveGoalsInProfile(
            user_id = user.id,
            profile_id = profile.id
        )
        save_to_db(db,goals_profile)
    
    return goals_profile




@router.get("/get_profiles", response_model = List[ProfileResponse])
def get_user_profiles(
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    return user.profiles
@router.get("/discover",response_model= List[ProfileResponse])
def get_public_profile(
    db:Session = Depends(get_db)
):
    public_profiles = db.query(Profile).filter(Profile.visible == 2).all()
    return public_profiles
@router.get("/get_active_profiles", response_model = List[ProfileResponse])
def get_user_active_profiles(
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    active_goals = db.query(ActiveGoalsInProfile).filter(ActiveGoalsInProfile.user_id == user.id).all()
# we will add a last use time to get the most recent active profiles later
    active_profiles = []
    for obj in active_goals:
        active_profiles.append(obj.profile)
    return active_profiles
@router.post("/createProfile", response_model=ProfileResponse)
def create_new_profile(
    user_session_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin users can create new profiles.")
    profile = get_draft_profile(user, db)
    if profile is None:
        profile = Profile(user_id=user.id)

        prompt = ProfilePrompt()
        profile.prompt = prompt

        save_to_db(db, profile)
             
    return profile
@router.get("/my_profile",response_model= List[ProfileResponse])
def get_my_created_profile(
    user_session_token: str = Cookie(None),
    db:Session = Depends(get_db)
):
    user = get_current_user(user_session_token, db)
    public_profiles = db.query(Profile).filter(Profile.user_id == user.id).all()
    return public_profiles
