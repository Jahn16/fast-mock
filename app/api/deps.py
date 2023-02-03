from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from jose.jwt import JWTError

from app.database import SessionLocal
from app.schemas.token import TokenData
from app.security import oauth2_scheme, decode_token
from app.crud.user import get_user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = get_user(db, token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
