from fastapi import APIRouter

from app.api.api_v1.endpoints import user, requests, login, mock_response

api_router = APIRouter()
api_router.include_router(login.router, prefix="/token", tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(
    requests.router, prefix="/requests", tags=["requests"]
)
api_router.include_router(mock_response.router, tags=["response"])
