from typing import Any

from pydantic import BaseModel, Field, Json


class RequestBase(BaseModel):
    endpoint: str


class RequestCreate(RequestBase):
    response: Json = Field(
        title="Mock Response",
        description="Response that will be returned when calling the endpoint",
        default=...,
    )

    class Config:
        schema_extra = {
            "example": {"endpoint": "/api/v1", "response": '{"test": 1}'}
        }


class RequestUpdate(RequestCreate):
    endpoint: str | None
    response: Json | None


class Request(RequestBase):
    id: int
    owner_id: int
    response: Any

    class Config:
        orm_mode = True
