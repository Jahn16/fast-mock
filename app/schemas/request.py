from typing import Any

from pydantic import BaseModel, Json


class RequestBase(BaseModel):
    endpoint: str


class RequestCreate(RequestBase):
    response: Json


class Request(RequestBase):
    id: int
    owner_id: int
    response: Any

    class Config:
        orm_mode = True
