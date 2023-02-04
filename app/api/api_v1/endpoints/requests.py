from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.request import Request, RequestCreate, RequestUpdate
from app.schemas.user import User
from app.crud import request as crud_request

router = APIRouter()


@router.get("/read", response_model=Request)
def read_request(
    request_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    request = crud_request.get_request_by_id(db, request_id, user.id)
    if not request:
        raise HTTPException(status_code=404, detail="Request Not Found")
    return request


@router.post("/create", response_model=Request)
def create_request(
    request: RequestCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud_request.create_request(db=db, request=request, user_id=user.id)


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
        raise HTTPException(status_code=404, detail="Request Not Found")
    return updated_request


@router.delete("/delete", response_model=Request)
def delete_request(
    request_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    request = crud_request.get_request_by_id(db, request_id, user.id)
    if not request:
        raise HTTPException(status_code=404, detail="Request Not Found")
    crud_request.delete_request(db, request)
    return request
