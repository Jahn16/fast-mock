import structlog
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.user import authenticate_user
from app.schemas.token import Token
from app.security import create_access_token

router = APIRouter()
logger = structlog.get_logger()


@router.post("", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(
            "Authentication error for user",
            user_email=form_data.username,
        )
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=str(user.id))
    logger.info("User logged in successfully", user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
