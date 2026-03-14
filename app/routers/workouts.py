from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session
from app.schemas import WorkoutCreate, WorkoutRead, WorkoutUpdate
from app.db import get_session
from app.services import (
    create_workout as service_create_workout,
    get_workout_by_id as service_get_workout_by_id,
    get_workouts_by_user_id as service_get_workouts_by_user_id,
    update_workout as service_update_workout,
    delete_workout as service_delete_workout
)
from app.models import User
from app.core.security import get_current_user

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.post("/", response_model=WorkoutRead, status_code=status.HTTP_201_CREATED)
def create_workout(
    payload: WorkoutCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return service_create_workout(session, payload, current_user)

@router.get("/", response_model=list[WorkoutRead])
def get_workouts(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return service_get_workouts_by_user_id(session, current_user)

@router.get("/{workout_id}", response_model=WorkoutRead)
def get_workout_by_id(
    workout_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return service_get_workout_by_id(session, workout_id, current_user)

@router.put("/{workout_id}", response_model=WorkoutRead)
def update_workout(
    workout_id: int,
    payload: WorkoutUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)

):
    return service_update_workout(session, payload, workout_id, current_user)

@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
    workout_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    service_delete_workout(session, workout_id, current_user)
    return None