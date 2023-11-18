from typing import Any

from pydantic import UUID4, BaseModel, Field, HttpUrl, Json


class RequestBase(BaseModel):
    pass


class RequestCreate(RequestBase):
    url: HttpUrl
    response: Json = Field(
        title="Mock Response",
        description="Response that will be returned when calling the endpoint",
        default=...,
    )

    class Config:
        schema_extra = {
            "example": {"url": "https://example.com/path", "response": '{"test": 1}'}
        }


class RequestUpdate(RequestBase):
    endpoint: str | None
    response: Json | None

    class Config:
        schema_extra = {
            "example": {"endpoint": "/path", "response": '{"test": 1}'}
        }


class Request(RequestBase):
    id: int
    endpoint: str
    owner_id: int
    url_id: UUID4
    response: dict | Any

    class Config:
        orm_mode = True
