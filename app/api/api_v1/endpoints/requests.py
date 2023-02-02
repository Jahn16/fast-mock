from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.request import Request, RequestCreate
from app.schemas.user import User
from app.crud import request as crud_request

router = APIRouter()


@router.post("/create", response_model=Request)
def create_request_for_user(
    request: RequestCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud_request.create_request(db=db, request=request, user_id=user.id)
