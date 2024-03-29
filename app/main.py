from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.config import settings
from app.middlewares.logger import LogMiddleware
from app.utils.logging import setup_logging

setup_logging()
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.1.0",
    description=(
        "Fast Mock is a very simple HTTP server mock, built using Fast API."
    ),
)

app.add_middleware(LogMiddleware)
app.include_router(api_router)
