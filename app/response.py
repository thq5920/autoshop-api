"""统一响应信封"""
from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None
    timestamp: int
    requestId: str = Field(alias="requestId")

    model_config = {"populate_by_name": True}


def _now_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def ok(data: Any = None, request_id: str = "") -> ApiResponse:
    return ApiResponse(
        code=200,
        message="success",
        data=data,
        timestamp=_now_ms(),
        requestId=request_id,
    )


def fail(code: int, message: str, request_id: str = "") -> ApiResponse:
    return ApiResponse(
        code=code,
        message=message,
        data=None,
        timestamp=_now_ms(),
        requestId=request_id,
    )
