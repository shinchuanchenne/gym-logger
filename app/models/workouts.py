from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, UTC, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .exercise_logs import ExerciseLog


class Workout(SQLModel, table=True):
    __tablename__ = "workouts"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    workout_date: date
    notes: str | None = Field(default=None)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    user: User = Relationship(back_populates="workouts")
    exercise_logs: list[ExerciseLog] = Relationship(back_populates="workout")