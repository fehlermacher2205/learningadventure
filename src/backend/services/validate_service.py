from models.user import User, UserSession
from models.profile import Profile
from models.story import Story, StoryPage
from models.goal_action import Action, Goal
import uuid
from models.job import Job
MODEL_REGISTRY = {
    "profile": Profile,
    "story": Story,
    "story_pages": StoryPage,
    "user": User,
    "goal": Goal,
    "job": Job,
    "user_session": UserSession,
    "action": Action
}
from sqlalchemy.orm import Session
from core.exceptions import ObjectNotFoundError, PermissionDeniedError
def validate_id(db: Session, model_class_name_in_registry, object_id: int, key_id_name_in_model:str):
    if model_class_name_in_registry not in MODEL_REGISTRY:
        raise ValueError(f"Developer Error: '{model_class_name_in_registry}' is not registered in MODEL_REGISTRY.")

    model_class = MODEL_REGISTRY[model_class_name_in_registry]
    
    instance = db.query(model_class).filter(getattr(model_class, key_id_name_in_model) == object_id).first()
    
    if not instance:
        raise ObjectNotFoundError(f"{model_class_name_in_registry.capitalize()} with {key_id_name_in_model} '{object_id}' not found.")
        
    return instance
def validate_string_id(db: Session, model_class_name_in_registry, object_id: str, key_id_name_in_model:str):
    if model_class_name_in_registry not in MODEL_REGISTRY:
        raise ValueError(f"Developer Error: '{model_class_name_in_registry}' is not registered in MODEL_REGISTRY.")

    model_class = MODEL_REGISTRY[model_class_name_in_registry]
    
    instance = db.query(model_class).filter(getattr(model_class, key_id_name_in_model) == object_id).first()
    
    if not instance:
        raise ObjectNotFoundError(f"{model_class_name_in_registry.capitalize()} with {key_id_name_in_model} '{object_id}' not found.")
        
    return instance

def check_story_ownership(user: User, story_id: str, db: Session):
    story = validate_id(db, "story", story_id, "id")
    if not story:
        raise ObjectNotFoundError(f"Story with id {story_id} not found.")
    if story.user_id != user.id:
        raise PermissionDeniedError(f"User does not have permission to access story with id {story_id}.")
    return story


#def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
 #   payload = decode_token(token)  # JWT decode
  #  user = db.query(User).filter(User.id == payload["user_id"]).first()
   # return user