from models.user import User , UserSession
from models.profile import Profile, ProfileStatus,MAX_QUESTION_NUM
from sqlalchemy.orm import Session
from models.profile import Profile
from db.database import get_db
import uuid
from datetime import datetime
from core.exceptions import (
    InvalidSessionError, 
    SessionExpiredError,
    ObjectNotFoundError,
    PermissionDeniedError
)
def is_user_session_active(
    session: UserSession, 
    timeout_minutes: int = 30
):
    if not session:
        return False
    timenow = datetime.utcnow()
    last_interaction = session.last_interaction
    if not last_interaction:
        return False
    if (timenow - last_interaction).total_seconds() > timeout_minutes * 60:
        return False
    return True
def get_current_user(
    user_session_token: str,
    db: Session,
):
    if not user_session_token:
        raise InvalidSessionError("No session token provided")
    user_session = db.query(UserSession).filter(
        UserSession.id == user_session_token
    ).first()

    if not user_session:
        raise InvalidSessionError("Invalid session")

    if not is_user_session_active(user_session):
        raise SessionExpiredError("Session expired")
    
    user_session.last_interaction = datetime.now()
    db.commit()
# if session is valid, always exists a user
    return db.query(User).filter(User.id == user_session.user_id).first()


def is_profile_visible_for_this_user(
    profile:Profile,
    user:User
):
# this profile is shared with link or public
    if profile.visible == ProfileStatus.private:
        return False
    return True
# TODO: we can add logic for for private link sharing later


def is_owner_of_profile(
    profile:Profile,
    user:User      
):
    if profile.user_id == user.id:
        return True
    return False



def create_user_session_login_token():
    return str(uuid.uuid4())

def validateOwnership(
    user: User,
    profile: Profile
):
    if user.id != profile.user_id:
        raise PermissionDeniedError("You do not have permission to access this profile")
    
def does_question_exist(
    profile: Profile,
    question_position: int
):
    
    if question_position < 1 or question_position > MAX_QUESTION_NUM:
        raise ObjectNotFoundError(f"Question position {question_position} is out of valid range")
    
    questions = profile.questions
    question = None
    for q in questions:
        if q.position == question_position:
            question = q
            break
    
    if question is None:
        raise ObjectNotFoundError(f"Question at position {question_position} does not exist")
    return question


def check_profile_visibility_for_user(
    profile: Profile,
    user: User
):  
    if profile.visible == ProfileStatus.private and profile.user_id != user.id:
        raise PermissionDeniedError("You do not have permission to access this profile")
    return True

def get_draft_profile(
    user:User,
    db: Session
):
    draft_profile = db.query(Profile).filter_by(user_id=user.id, visible=ProfileStatus.draft).first()
    return draft_profile
