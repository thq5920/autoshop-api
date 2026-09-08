"""统一响应信封"""
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field

from app import i18n


class ApiResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None
    timestamp: int
    requestId: str = Field(alias="requestId")

    model_config = {"populate_by_name": True}


def _now_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def _new_request_id() -> str:
    """默认 requestId 生成器。未显式传入时,所有成功响应也带 `req_` 前缀,
    与 JSON Schema 中的 ^req_ 正则约束保持一致。
    """
    return f"req_{uuid.uuid4().hex[:16]}"


def ok(data: Any = None, request_id: str | None = None,
       locale: str = i18n.DEFAULT) -> ApiResponse:
    rid = request_id if request_id else _new_request_id()
    return ApiResponse(
        code=200,
        message=i18n.msg(200, locale),
        data=data,
        timestamp=_now_ms(),
        requestId=rid,
    )


def fail(code: int, message: str, request_id: str | None = None,
         locale: str = i18n.DEFAULT) -> ApiResponse:
    rid = request_id if request_id else _new_request_id()
    return ApiResponse(
        code=code,
        message=message or i18n.msg(code, locale),
        data=None,
        timestamp=_now_ms(),
        requestId=rid,
    )
