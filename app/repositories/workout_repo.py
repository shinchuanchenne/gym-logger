from sqlmodel import Session, select
from app.models import Workout

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
) -> list[Workout]:
    statement = select(Workout).where(Workout.user_id == user_id)
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
