import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    netloc = Column(String, index=True)
    requests = relationship("Request", back_populates="url")



