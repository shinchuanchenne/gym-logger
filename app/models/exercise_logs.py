from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, UTC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .workouts import Workout

class ExerciseLog(SQLModel, table=True):
    __tablename__ = "exercise_logs"

    id: int | None = Field(default=None, primary_key=True)
    exercise_name: str
    sets: int
    reps: int
    weight: float
    notes: str | None = Field(default=None)
    workout_id: int = Field(foreign_key="workouts.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    workout: Workout = Relationship(back_populates="exercise_logs")