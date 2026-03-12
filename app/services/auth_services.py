from sqlmodel import Session
from app.repositories.user_repo import (
    get_user_by_email
)
from app.core.security import verify_password, create_access_token
from app.models import User

def authenticate_user(session: Session, form_email: str, form_password: str) -> User | None:

    user = get_user_by_email(session, form_email)
    if not user:
        return None    
    is_valid_password = verify_password(form_password, user.hashed_password)
    if not is_valid_password:
        return None    
    return user