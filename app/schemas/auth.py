from pydantic import BaseModel, Field, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=256)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str