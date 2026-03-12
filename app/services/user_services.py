from sqlmodel import Session
from app.schemas import UserCreate, UserUpdate
from app.repositories.user_repo import (
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
    create_user as create_user_repo,
)
from app.models import User
from app.core.security import hash_password
from fastapi import HTTPException, status

def create_user(session: Session, payload: UserCreate) -> User:
    data = payload.model_dump()
    
    existing_email = get_user_by_email(session, payload.email)
    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    existing_username = get_user_by_username(session, payload.username)
    if existing_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")
    
    hashed_password = hash_password(payload.password)
    data.pop("password")
    data["hashed_password"] = hashed_password

    user = create_user_repo(session, data)
    return user

    

    

