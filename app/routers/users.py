from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from app.schemas import UserCreate, UserRead
from app.db.session import get_session
from app.services import create_user as service_create_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    session: Session = Depends(get_session)
):
    return service_create_user(session, payload)