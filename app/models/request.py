from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, index=True)
    response = Column(JSONB, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    url_id = Column(UUID, ForeignKey("urls.id"))

    owner = relationship("User", back_populates="requests")
    url = relationship("URL", back_populates="requests")
