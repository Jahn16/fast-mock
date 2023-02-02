from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.crud.user import (
    get_users,
    get_user,
    get_user_by_email,
    create_user,
    authenticate_user,
)
from app.crud.request import get_requests, create_request, get_request
from app.schemas.user import User, UserCreate
from app.schemas.request import Request, RequestCreate
from app.schemas.token import Token
from app.database import Base, engine
from app.deps import get_db, get_current_user
from app.security import create_access_token


Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.post("/users/requests/", response_model=Request)
def create_request_for_user(
    request: RequestCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_request(db=db, request=request, user_id=user.id)


@app.get("/requests/", response_model=list[Request])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_requests(db, skip=skip, limit=limit)
    return items


@app.post("/token", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/{mock_endpoint:path}")
@app.post("/{mock_endpoint:path}")
def read_request_response(
    mock_endpoint: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    request = get_request(db, user.id, endpoint=mock_endpoint)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request.response
