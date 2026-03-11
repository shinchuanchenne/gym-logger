from sqlmodel import SQLModel, Field
from datetime import datetime, UTC, date


class Workout(SQLModel, table=True):
    __tablename__ = "workouts"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    workout_date: date
    notes: str | None = Field(default=None)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))