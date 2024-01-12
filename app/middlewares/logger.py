from typing import Any

import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger(__name__)


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Any) -> Any:
        logger.info(
            "Incoming request",
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host,  # type: ignore
        )

        response = await call_next(request)
        return response
