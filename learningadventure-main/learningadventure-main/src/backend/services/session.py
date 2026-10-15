from sqlalchemy.orm import Session
from models.user import User

from services.utility import save_to_db

from models.profile import Profile


from models.story import Story



    
def create_story_session(
    profile:Profile,    
    db: Session ,
    user: User
)->Story:
    
    new_session = Story(
        user_id = user.id,
        profile_id = profile.id
    )
    save_to_db(db, new_session)
    return new_session

