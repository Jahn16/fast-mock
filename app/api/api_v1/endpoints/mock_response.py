from typing import Any

import structlog
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request as StarletteRequest
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.request import filter_requests, match_best_request

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
    requests = filter_requests(
        db,
        url_id=url_id,
        method=starlette_request.method,
        endpoint=f"/{mock_endpoint}",
    )
    if not requests:
        logger.info("Request not found", url_id=url_id)
        raise HTTPException(status_code=404, detail="Request not found")

    logger.debug(str(starlette_request.query_params))
    request = match_best_request(requests, str(starlette_request.query_params))
    logger.info(
        "Sending mocked response for request",
        request_id=request.id,
        url_id=url_id,
    )
    return request.response
