from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.security import get_password_hash, verify_password


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email, hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_in: UserUpdate, user_id: int) -> None:
    data = user_in.dict(exclude_unset=True)
    if "password" in data:
        data["hashed_password"] = get_password_hash(data.pop("password"))
    db.query(User).filter(User.id == user_id).update(data)  # type: ignore
    db.commit()


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


def authenticate_user(
    db: Session, username: str, password: str
) -> User | None:
    user = get_user_by_email(db, username)
    if not user:
        return None
    if not verify_password(password, str(user.hashed_password)):
        return None
    return user
