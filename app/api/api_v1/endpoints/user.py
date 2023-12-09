import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud import user as crud_user
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()
logger = structlog.get_logger()


@router.get("/read", response_model=User)
def read_user(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    db_user = crud_user.get_user(db, user_id=user.id)
    if not db_user:
        logger.warning("User not found", user_id=user.id)
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("Retrieved user", user_id=db_user.id)
    return db_user


@router.post("/create", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        logger.warning(
            "Email already registered by another user",
            user_email=user.email,
        )
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud_user.create_user(db=db, user=user)
    logger.info("Created user", user_id=db_user.id)
    return db_user


@router.put("/update", response_model=User)
def update_user(
    user_in: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crud_user.update_user(db, user_in, user.id)
    db_user = crud_user.get_user(db, user.id)
    if not db_user:
        logger.warning("User not found while updating", user_id=user.id)
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("Updated user", user_id=user.id)
    return db_user


@router.delete("/delete", response_model=User)
def delete_user(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    crud_user.delete_user(db, user)
    logger.info("Deleted user", user_id=user.id)
    return user
