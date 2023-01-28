from pydantic import BaseModel


class RequestBase(BaseModel):
    endpoint: str
    response: str


class RequestCreate(RequestBase):
    pass


class Request(RequestBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
