from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlmodel import Session
from app.schemas import WorkoutCreate, WorkoutRead, WorkoutUpdate, WorkoutDetailRead
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
from datetime import date

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
    workout_date: date | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return service_get_workouts_by_user_id(
        session,
        current_user,
        workout_date=workout_date,
        limit=limit,
        offset=offset,
    )

@router.get("/{workout_id}", response_model=WorkoutDetailRead)
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