from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session
from app.schemas import UserCreate, UserRead, UserUpdate
from app.db.session import get_session
from app.services import (
    create_user as service_create_user,
    update_user as service_update_user,
)
from app.models import User
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    session: Session = Depends(get_session)
):
    return service_create_user(session, payload)

@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserRead)
def update_user(
    payload: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user = service_update_user(session, payload, current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user