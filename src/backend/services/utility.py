from requests import Session
from core.exceptions import PermissionDeniedError
# NOTE:
# Do not import self defined packages here
# This file exists to solve cicular import issues


from sqlalchemy.orm import Session
def save_to_db(db: Session, obj):
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
    except Exception:
        db.rollback()
        raise PermissionDeniedError("Forbidden behavior in database")
