from sqlmodel import Session, select
from app.models import User

def create_user(
        session: Session,
        data: dict,
) -> User:
    user = User(**data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_email(
        session: Session,
        email: str,
) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_username(
        session: Session,
        username: str,
) -> User | None:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def get_user_by_id(
        session: Session,
        user_id: int,
) -> User | None:
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()

def update_user(
        session: Session,
        user_id: int,
        updated_data: dict,
) -> User | None:
    user = get_user_by_id(session, user_id)

    if not user:
        return None
    
    for key, value in updated_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user