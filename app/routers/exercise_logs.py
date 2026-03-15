from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.schemas import ExerciseLogCreate, ExerciseLogRead, ExerciseLogUpdate
from app.db import get_session
from app.services import (
    create_exercise_log as service_create_exercise_log,
    get_exercise_log_by_id as service_get_exercise_log_by_id,
    get_exercise_logs_by_workout_id as service_get_exercise_logs_by_workout_id,
    update_exercise_log as service_update_exercise_log,
    delete_exercise_log as service_delete_exercise_log
)
from app.models import User
from app.core.security import get_current_user

router = APIRouter(tags=["exercise-logs"])

@router.post("/workouts/{workout_id}/exercise-logs", response_model=ExerciseLogRead, status_code=status.HTTP_201_CREATED)
def create_exercise_log(
    payload: ExerciseLogCreate,
    workout_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return service_create_exercise_log(session, payload, workout_id, current_user)

@router.get("/workouts/{workout_id}/exercise-logs", response_model=list[ExerciseLogRead])
def get_exercise_logs(
    workout_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),

):
    return service_get_exercise_logs_by_workout_id(session, workout_id, current_user)

@router.get("/workouts/{workout_id}/exercise-logs/{exercise_log_id}", response_model=ExerciseLogRead)
def get_exercise_log_by_id(
    workout_id: int,
    exercise_log_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return service_get_exercise_log_by_id(session,workout_id, exercise_log_id, current_user)

@router.put("/workouts/{workout_id}/exercise-logs/{exercise_log_id}", response_model=ExerciseLogRead)
def update_exercise_log(
    workout_id: int,
    exercise_log_id: int,
    payload: ExerciseLogUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return service_update_exercise_log(session, payload, workout_id, exercise_log_id, current_user)

@router.delete("/workouts/{workout_id}/exercise-logs/{exercise_log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise_log(
    workout_id: int,
    exercise_log_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    service_delete_exercise_log(session, exercise_log_id, workout_id, current_user)
    return None