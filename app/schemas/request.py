from typing import Any, Literal

from pydantic import UUID4, BaseModel, Field, HttpUrl, Json


class RequestBase(BaseModel):
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    status_code: int = Field(ge=100, le=511, default=...)


class RequestCreate(RequestBase):
    url: HttpUrl
    response: Json[Any] = Field(
        title="Mock Response",
        description="Response that will be returned when calling the endpoint",
        default=...,
    )

    class Config:
        schema_extra = {
            "example": {
                "method": "GET",
                "url": "https://example.com/path?param1=foo&param2=bar",
                "status_code": 200,
                "response": '{"test": 1}',
            }
        }


class RequestUpdate(RequestBase):
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] | None  # type: ignore[assignment] # noqa: E501
    status_code: int | None = Field(ge=100, le=511, default=None)  # type: ignore[assignment] # noqa: E501
    endpoint: str | None
    parameters: str | None
    response: Json[Any] | None

    class Config:
        schema_extra = {
            "example": {
                "method": "GET",
                "endpoint": "/path",
                "parameters": "param1=foo&param2=bar",
                "status_code": 200,
                "response": '{"test": 1}',
            }
        }


class Request(RequestBase):
    id: int
    endpoint: str
    parameters: str = ""
    owner_id: int
    url_id: UUID4
    response: dict[Any, Any] | Any

    class Config:
        orm_mode = True
