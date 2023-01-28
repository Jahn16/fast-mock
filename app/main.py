from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.crud.user import get_users, get_user, get_user_by_email, create_user
from app.crud.request import get_requests, create_request, get_request
from app.schemas.user import User, UserCreate
from app.schemas.request import Request, RequestCreate
from app.database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=User)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/requests/", response_model=Request)
def create_request_for_user(
    user_id: int, request: RequestCreate, db: Session = Depends(get_db)
):
    return create_request(db=db, request=request, user_id=user_id)


@app.get("/requests/", response_model=list[Request])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_requests(db, skip=skip, limit=limit)
    return items


@app.get("/{mock_endpoint:path}")
@app.post("/{mock_endpoint:path}")
def read_request_response(
    mock_endpoint: str, user_id: int, db: Session = Depends(get_db)
):
    request = get_request(db, user_id, endpoint=mock_endpoint)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request.response
