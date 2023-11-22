from typing import Any, Literal

from pydantic import UUID4, BaseModel, Field, HttpUrl, Json


class RequestBase(BaseModel):
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


class RequestCreate(RequestBase):
    url: HttpUrl
    response: Json = Field(
        title="Mock Response",
        description="Response that will be returned when calling the endpoint",
        default=...,
    )

    class Config:
        schema_extra = {
            "example": {
                "method": "GET",
                "url": "https://example.com/path?param1=foo&param2=bar",
                "response": '{"test": 1}',
            }
        }


class RequestUpdate(RequestBase):
    method: str | None
    endpoint: str | None
    parameters: str | None
    response: Json | None

    class Config:
        schema_extra = {
            "example": {
                "endpoint": "/path",
                "parameters": "param1=foo&param2=bar",
                "response": '{"test": 1}',
            }
        }


class Request(RequestBase):
    id: int
    endpoint: str
    parameters: str = ""
    owner_id: int
    url_id: UUID4
    response: dict | Any

    class Config:
        orm_mode = True
