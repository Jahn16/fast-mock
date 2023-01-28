from sqlalchemy.orm import Session

from app import schemas
from app.models.request import Request


def get_request(db: Session, user_id: int, endpoint: str) -> Request:
    return (
        db.query(Request)
        .filter(Request.owner_id == user_id, Request.endpoint == endpoint)
        .first()
    )


def get_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Request).offset(skip).limit(limit).all()


def create_request(
    db: Session, request: schemas.request.RequestCreate, user_id: int
):
    db_item = Request(**request.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
