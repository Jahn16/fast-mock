from sqlalchemy.orm import Session

from app.schemas.request import RequestCreate, RequestUpdate
from app.models.request import Request


def get_request_by_id(db: Session, request_id: int, user_id: int) -> Request:
    return (
        db.query(Request)
        .filter(Request.owner_id == user_id, Request.id == request_id)
        .first()
    )


def get_request(db: Session, url_id: str, endpoint: str) -> Request:
    print(url_id)
    return (
        db.query(Request)
        .filter(Request.url_id == url_id, Request.endpoint == endpoint)
        .first()
    )


def get_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Request).offset(skip).limit(limit).all()


def create_request(db: Session, request: RequestCreate, user_id: int, url_id: str):
    db_request = Request(
        endpoint=request.url.path,
        response=request.response,
        owner_id=user_id,
        url_id=url_id,
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def update_request(db: Session, request_in: Request, request_id: int, user_id: int):
    (
        db.query(Request)
        .filter(Request.owner_id == user_id, Request.id == request_id)
        .update(request_in.dict(exclude_unset=True))
    )
    db.commit()


def delete_request(db: Session, request: Request):
    db.delete(request)
    db.commit()
