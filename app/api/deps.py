from typing import Generator

import structlog
from fastapi import Depends, HTTPException
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from app.crud.user import get_user
from app.database import SessionLocal
from app.models.user import User
from app.schemas.token import TokenData
from app.security import decode_token, oauth2_scheme

logger = structlog.get_logger()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id = payload.get("sub", "")
        if not user_id:
            logger.warning("User not logged in")
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        logger.warning("User not logged in")
        raise credentials_exception

    user = get_user(db, int(token_data.user_id) if token_data.user_id else -1)
    if user is None:
        logger.warning("User do not exist anymore")
        raise credentials_exception
    return user
