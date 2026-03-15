from sqlmodel import Session
from app.schemas import ExerciseLogCreate, ExerciseLogUpdate
from app.repositories import (
    get_workout_by_id as get_workout_by_id_repo,
    get_exercise_log_by_id as get_exercise_log_by_id_repo,
    get_exercise_logs_by_workout_id as get_exercise_logs_by_workout_id_repo,
    create_exercise_log as create_exercise_log_repo,
    update_exercise_log as update_exercise_log_repo,
    delete_exercise_log as delete_exercise_log_repo,
)
from app.models import ExerciseLog, Workout, User
from fastapi import HTTPException, status


def check_workout_owner(
        session: Session,
        workout_id: int,
        current_user: User,
) -> Workout:
    workout = get_workout_by_id_repo(session, workout_id)
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this workout")
    return workout

def check_exercise_owner(
        session: Session,
        exercise_log_id: int,
        current_user: User,
) -> ExerciseLog:
    # grab this exercise_id's workout_id
    exercise_log = get_exercise_log_by_id_repo(session, exercise_log_id)
    if not exercise_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise log not found")
    # workout_id
    workout_id = exercise_log.workout_id
    # grab this work_id's user_id
    check_workout_owner(session, workout_id, current_user)
    return exercise_log

def create_exercise_log(
        session: Session,
        payload: ExerciseLogCreate,
        workout_id: int,
        current_user: User
) -> ExerciseLog:
    check_workout_owner(session, workout_id, current_user)
    data = payload.model_dump()
    data["workout_id"] = workout_id
    return create_exercise_log_repo(session, data)


def get_exercise_logs_by_workout_id(
        session: Session,
        workout_id: int,
        current_user: User
) -> list[ExerciseLog]:
    check_workout_owner(session, workout_id, current_user)
    return get_exercise_logs_by_workout_id_repo(session, workout_id)


def get_exercise_log_by_id(
        session: Session,
        workout_id: int,
        exercise_log_id: int,
        current_user: User
) -> ExerciseLog:
    data = get_exercise_log_by_id_repo(session, exercise_log_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise log not found")
    
    # check exercise belongs to workout
    # check workout belongs to user
    check_exercise_owner(session, exercise_log_id, current_user)

    if data.workout_id != workout_id:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Exercise log not found in this workout",
    )
    check_workout_owner(session, workout_id, current_user)

    return data

def update_exercise_log(
        session: Session,
        payload: ExerciseLogUpdate,
        workout_id: int,
        exercise_log_id: int,
        current_user: User
) -> ExerciseLog:
    data = payload.model_dump(exclude_unset=True)

    # check workout id s true
    db_data = get_exercise_log_by_id_repo(session, exercise_log_id)
    # if not return 404
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise log not found")
    # check user has authorication to update, if not return 403
    check_exercise_owner(session, exercise_log_id, current_user)
    if db_data.workout_id != workout_id:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Exercise log not found in this workout",
    )
    check_workout_owner(session, workout_id, current_user)

    return update_exercise_log_repo(session, exercise_log_id, data)

def delete_exercise_log(
        session: Session,
        exercise_log_id: int,
        workout_id: int,
        current_user: User
) -> bool:
    db_data = get_exercise_log_by_id_repo(session, exercise_log_id)
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise log not found")
    check_exercise_owner(session, exercise_log_id, current_user)
    if db_data.workout_id != workout_id:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Exercise log not found in this workout",
    )
    check_workout_owner(session, workout_id, current_user)

    return delete_exercise_log_repo(session, exercise_log_id)