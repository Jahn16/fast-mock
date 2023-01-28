from pydantic import BaseModel, EmailStr

from app.schemas.request import Request


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(BaseModel):
    password: str


class User(UserBase):
    id: int
    requests: list[Request] = []

    class Config:
        orm_mode = True
