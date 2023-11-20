from typing import Any

import structlog
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request as StarletteRequest
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.request import get_request

router = APIRouter()
logger = structlog.get_logger()


@router.get("/{mock_endpoint:path}")
@router.post("/{mock_endpoint:path}")
def read_request_response(
    mock_endpoint: str,
    starlette_request: StarletteRequest,
    db: Session = Depends(get_db),
) -> dict | Any:
    hostname = starlette_request.url.hostname or ""
    url_id = hostname.split(".")[0]
    request = get_request(db, url_id=url_id, endpoint=f"/{mock_endpoint}")
    if not request:
        logger.info("Request not found", url_id=url_id)
        raise HTTPException(status_code=404, detail="Request not found")
    logger.info(
        "Sending mocked response for request",
        request_id=request.id,
        url_id=url_id,
    )
    return request.response
