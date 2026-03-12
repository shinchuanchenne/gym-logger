from sqlmodel import Session
from app.repositories.user_repo import (
    get_user_by_email
)
from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token

def authenticate_user(session: Session, form_email: str, form_password: str) -> dict:

    user = get_user_by_email(session, form_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    
    is_valid_password = verify_password(form_password, user.hashed_password)
    if not is_valid_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    
    access_token = create_access_token({"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }