from sqlmodel import Session
from app.schemas import UserCreate, UserUpdate
from app.repositories.user_repo import (
    get_user_by_email as get_user_by_email_repo,
    get_user_by_id as get_user_by_id_repo,
    get_user_by_username as get_user_by_username_repo,
    create_user as create_user_repo,
    update_user as update_user_repo,
)
from app.models import User
from app.core.security import hash_password
from fastapi import HTTPException, status

def create_user(session: Session, payload: UserCreate) -> User:
    data = payload.model_dump()
    
    existing_email = get_user_by_email_repo(session, payload.email)
    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    existing_username = get_user_by_username_repo(session, payload.username)
    if existing_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")
    
    hashed_password = hash_password(payload.password)
    data.pop("password")
    data["hashed_password"] = hashed_password

    user = create_user_repo(session, data)
    return user

    
def get_current_user_profile(
        session: Session,
        current_user: User,
) -> User | None:
    user_id = current_user.id
    return get_user_by_id_repo(session, user_id)
    

def update_user(
        session: Session,
        payload: UserUpdate,
        user_id: int,
) -> User | None:
    data = payload.model_dump(exclude_unset=True)
    # Check email
    if "email" in data:
        existing_email = get_user_by_email_repo(session, data["email"])
        if existing_email and existing_email.id != user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered.")
        
    # Check username
    if "username" in data:
        existing_username = get_user_by_username_repo(session, data["username"])
        if existing_username and existing_username.id != user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered.")
    
    # hash password
    if "password" in data:
        hashed_password = hash_password(data["password"])
        data.pop("password")
        data["hashed_password"] = hashed_password

    return update_user_repo(session, user_id, data)