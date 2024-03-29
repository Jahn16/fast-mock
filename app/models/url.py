import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hostname = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    requests = relationship("Request", back_populates="url")
    owner = relationship("User", back_populates="urls")
