import uuid
from sqlalchemy.orm import Session

from app.schemas.request import RequestCreate, RequestUpdate
from app.models.request import Request
from urllib.parse import parse_qs


def match_best_request(requests: list[Request], parameters: str) -> Request:
    if not requests:
        raise ValueError("Need at least 1 request to match")

    desired_parameters = parse_qs(parameters)

    def matching_score(request: Request) -> int:
        request_parameters = parse_qs(str(request.parameters))
        if not desired_parameters:
            return 100 // (len(request_parameters) + 1)
        score = 0
        for key, value in request_parameters.items():
            if desired_parameters.get(key) == value:
                score += 1
        percentage = (
            round(score / len(request_parameters) * 100)
            if request_parameters
            else 0
        )
        return percentage

    max_score = -1
    best_request = requests[0]
    logger.debug(desired_parameters)
    for request in requests:
        score = matching_score(request)
        if score > max_score:
            max_score = score
            best_request = request
    return best_request


def validate_uuid(value: str):
    try:
        uuid.UUID(value)
    except ValueError:
        return False
    return True


def get_request_by_id(
    db: Session, request_id: int, user_id: int
) -> Request | None:
    return (
        db.query(Request)
        .filter(Request.owner_id == user_id, Request.id == request_id)
        .first()
    )


def filter_requests(
    db: Session, url_id: str, method: str, endpoint: str
) -> list[Request]:
    if not validate_uuid(url_id):
        return []
    return list(
        db.query(Request).filter(
            Request.url_id == url_id,
            Request.method == method,
            Request.endpoint == endpoint,
        )
    )


def get_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Request).offset(skip).limit(limit).all()


def create_request(
    db: Session, request: RequestCreate, user_id: int, url_id: str
):
    db_request = Request(
        method=request.method,
        endpoint=request.url.path,
        parameters=request.url.query or "",
        response=request.response,
        owner_id=user_id,
        url_id=url_id,
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def update_request(
    db: Session, request_in: Request, request_id: int, user_id: int
):
    (
        db.query(Request)
        .filter(Request.owner_id == user_id, Request.id == request_id)
        .update(request_in.dict(exclude_unset=True))
    )
    db.commit()


def delete_request(db: Session, request: Request):
    db.delete(request)
    db.commit()
