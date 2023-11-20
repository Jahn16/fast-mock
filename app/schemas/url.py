from pydantic import UUID4, BaseModel


class URL(BaseModel):
    id: UUID4
    hostname: str

    class Config:
        orm_mode = True
