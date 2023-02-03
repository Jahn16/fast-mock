from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/api/v1")
