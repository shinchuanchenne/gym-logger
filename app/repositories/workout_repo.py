from sqlmodel import Session, select
from app.models import Workout
from datetime import date

def create_workout(
        session: Session,
        data: dict
) -> Workout:
    workout = Workout(**data)
    session.add(workout)
    session.commit()
    session.refresh(workout)
    return workout


def get_workouts_by_user_id(
        session: Session,
        user_id: int,
        workout_date: date | None = None,
        limit: int = 10,
        offset: int = 0,
) -> list[Workout]:
    statement = select(Workout).where(Workout.user_id == user_id)

    if workout_date is not None:
        statement = statement.where(Workout.workout_date == workout_date)
    statement = statement.offset(offset).limit(limit)
    return session.exec(statement).all()

    

def get_workout_by_id(
        session: Session,
        workout_id: int,
) -> Workout | None:
    statement = select(Workout).where(Workout.id == workout_id)
    return session.exec(statement).first()


def update_workout(
        session: Session,
        workout_id: int,
        updated_data: dict,
) -> Workout | None:
    workout = get_workout_by_id(session, workout_id)

    if not workout:
        return None
    
    for key, value in updated_data.items():
        setattr(workout, key, value)
    session.add(workout)
    session.commit()
    session.refresh(workout)
    return workout


def delete_workout(
        session: Session,
        workout_id: int,
) -> bool:
    workout = get_workout_by_id(session, workout_id)

    if not workout:
        return False
    session.delete(workout)
    session.commit()
    return True
