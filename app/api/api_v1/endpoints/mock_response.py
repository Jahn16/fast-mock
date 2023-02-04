from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.user import User
from app.crud.request import get_request

router = APIRouter()


@router.get("/{mock_endpoint:path}")
@router.post("/{mock_endpoint:path}")
def read_request_response(
    mock_endpoint: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    request = get_request(db, user.id, endpoint=mock_endpoint)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request.response
