from pydantic import BaseModel, EmailStr

from app.schemas.request import Request
from app.schemas.url import URL


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: EmailStr | None  # type: ignore[assignment]
    password: str | None


class User(UserBase):
    id: int
    requests: list[Request] = []
    urls: list[URL] = []

    class Config:
        orm_mode = True
