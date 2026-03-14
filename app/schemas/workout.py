from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date

class WorkoutCreate(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    workout_date: date
    notes: str | None = Field(default=None, max_length=512)

class WorkoutRead(BaseModel):
    id: int
    title: str
    workout_date: date
    notes: str | None = None
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class WorkoutUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=64)
    workout_date: date | None = None
    notes: str | None = Field(default=None, max_length=512)