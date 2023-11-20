import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.request import Request, RequestCreate, RequestUpdate
from app.schemas.user import User
from app.crud import request as crud_request
from app.crud import url as crud_url

router = APIRouter()
logger = structlog.get_logger()


@router.get("/read", response_model=Request)
def read_request(
    request_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    request = crud_request.get_request_by_id(db, request_id, user.id)
    if not request:
        logger.info("Request not found", request_id=request_id)
        raise HTTPException(status_code=404, detail="Request Not Found")
    logger.info("Retrieved request", request_id=request_id, user_id=user.id)
    return request


@router.post("/create", response_model=Request)
def create_request(
    request: RequestCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_url = crud_url.get_url(db, request.url, user.id)
    if not db_url:
        db_url = crud_url.create_url(db, request.url, user.id)
        logger.info(f"Created url for {request.url}", url_id=db_url.id)
    request = crud_request.create_request(
        db=db, request=request, user_id=user.id, url_id=str(db_url.id)
    )
    logger.info(
        "Created request",
        request_id=request.id,
        url_id=db_url.id,
        user_id=user.id,
    )
    return request


@router.put("/update", response_model=Request)
def update_request(
    request_id: int,
    request_in: RequestUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crud_request.update_request(db, request_in, request_id, user.id)
    updated_request = crud_request.get_request_by_id(db, request_id, user.id)
    if not updated_request:
        logger.warning(
            "Request not found for updating",
            request_id=request_id,
            user_id=user.id,
        )
        raise HTTPException(status_code=404, detail="Request Not Found")
    logger.info("Updated request", request_id=request_id, user_id=user.id)
    return updated_request


@router.delete("/delete", response_model=Request)
def delete_request(
    request_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    request = crud_request.get_request_by_id(db, request_id, user.id)
    if not request:
        logger.warning(
            "Request not found for deleting",
            request_id=request_id,
            user_id=user.id,
        )
        raise HTTPException(status_code=404, detail="Request Not Found")
    crud_request.delete_request(db, request)
    logger.info("Deleted request", request_id=request_id, user_id=user.id)
    return request
