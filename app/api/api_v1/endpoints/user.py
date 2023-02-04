from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.user import User, UserCreate, UserUpdate
from app.crud import user as crud_user


router = APIRouter()


@router.get("/read", response_model=User)
def read_user(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    db_user = crud_user.get_user(db, user_id=user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/create", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.put("/update", response_model=User)
def update_user(
    user_in: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crud_user.update_user(db, user_in, user.id)
    db_user = crud_user.get_user(db, user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/delete", response_model=User)
def delete_user(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    crud_user.delete_user(db, user)
    return user
