from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ExerciseLogCreate(BaseModel):
    exercise_name: str = Field(min_length=1, max_length=64)
    sets: int = Field(ge=1, le=999)
    reps: int = Field(ge=1, le=999)
    weight: float = Field(ge=0, le=999)
    notes: str | None = Field(default=None, max_length=512)

class ExerciseLogRead(BaseModel):
    id: int
    exercise_name: str
    sets: int
    reps: int
    weight: float
    notes: str | None = None
    workout_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ExerciseLogUpdate(BaseModel):
    exercise_name: str | None = Field(default=None, min_length=1, max_length=64)
    sets: int | None = Field(default=None, ge=1, le=999)
    reps: int | None = Field(default=None, ge=1, le=999)
    weight: float | None = Field(default=None, ge=0, le=999)
    notes: str | None = Field(default=None, max_length=512)