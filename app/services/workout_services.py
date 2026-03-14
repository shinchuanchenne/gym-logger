from sqlmodel import Session
from app.schemas import WorkoutCreate, WorkoutUpdate
from app.repositories import (
    get_workout_by_id as get_workout_by_id_repo,
    get_workouts_by_user_id as get_workouts_by_user_id_repo,
    create_workout as create_workout_repo,
    update_workout as update_workout_repo,
    delete_workout as delete_workout_repo, 
)
from app.models import Workout, User

def create_workout(
        session: Session,
        payload: WorkoutCreate,
        current_user: User,
) -> Workout:
    data = payload.model_dump()
    data["user_id"] = current_user.id
    return create_workout_repo(session, data)



def get_workouts_by_user_id(
        session: Session,
        current_user: User,
) -> list[Workout]:
    user_id = current_user.id
    return get_workouts_by_user_id_repo(session, user_id)

def get_workout_by_id(
        session: Session,
        workout_id: int,
) -> Workout | None:
    return get_workout_by_id_repo(session, workout_id)

def update_workout(
        session: Session,
        payload: WorkoutUpdate,
        workout_id: int,
) -> Workout | None:
    updated_data = payload.model_dump(exclude_unset=True)
    return update_workout_repo(session, workout_id, updated_data)

def delete_workout(
        session: Session,
        workout_id: int,
) -> bool:
    return delete_workout_repo(session, workout_id)