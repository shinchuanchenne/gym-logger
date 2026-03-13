from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, UTC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .workouts import Workout

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    workouts: list["Workout"] = Relationship(back_populates="user")