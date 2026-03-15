from sqlmodel import Session, select
from app.models import ExerciseLog

def create_exercise_log(
        session: Session,
        data: dict,
) -> ExerciseLog:
    exercise_log = ExerciseLog(**data)
    session.add(exercise_log)
    session.commit()
    session.refresh(exercise_log)
    return exercise_log
    

def get_exercise_logs_by_workout_id(
        session: Session,
        workout_id: int,
) -> list[ExerciseLog]:
    statement = select(ExerciseLog).where(ExerciseLog.workout_id == workout_id)
    return session.exec(statement).all()


def get_exercise_log_by_id(
        session: Session,
        exercise_log_id: int,
) -> ExerciseLog | None:
    statement = select(ExerciseLog).where(ExerciseLog.id == exercise_log_id)
    return session.exec(statement).first()


def update_exercise_log(
        session: Session,
        exercise_log_id: int,
        updated_data: dict,
) -> ExerciseLog | None:
    exercise_log = get_exercise_log_by_id(session, exercise_log_id)

    if not exercise_log:
        return None
    for key, value in updated_data.items():
        setattr(exercise_log, key, value)
    session.add(exercise_log)
    session.commit()
    session.refresh(exercise_log)
    return exercise_log

def delete_exercise_log(
        session: Session,
        exercise_log_id: int,
) -> bool:
    exercise_log = get_exercise_log_by_id(session, exercise_log_id)
    if not exercise_log:
        return False
    session.delete(exercise_log)
    session.commit()
    return True