from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    email: EmailStr
    password: str = Field(min_length=8, max_length=256)


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=64)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=256)

