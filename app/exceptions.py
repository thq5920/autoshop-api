"""业务异常 + 统一异常处理"""
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.response import ApiResponse


class BizException(Exception):
    """业务异常:code 为业务码,http_status 为 HTTP 状态码"""

    def __init__(self, code: int, message: str, http_status: int = 400):
        self.code = code
        self.message = message
        self.http_status = http_status


# 业务码常量(文档第 2 节)
class BizCode:
    SUCCESS = 200
    PARAM_INVALID = 40001      # 参数错误
    PARAM_MISSING = 40002      # 参数缺失
    PRODUCT_OFF_SHELF = 40003  # 商品已下架
    UNAUTHORIZED = 40101       # 未登录
    TOKEN_INVALID = 40102      # Token 无效
    TOKEN_EXPIRED = 40103      # Token 已过期
    NOT_FOUND = 40401          # 数据不存在
    CONFLICT = 40901           # 数据已存在
    SYSTEM_ERROR = 50001       # 系统异常


def _new_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:16]}"


async def biz_exception_handler(request: Request, exc: BizException):
    return JSONResponse(
        status_code=exc.http_status,
        content=ApiResponse(
            code=exc.code,
            message=exc.message,
            data=None,
            timestamp=_now_ms(),
            requestId=_new_request_id(),
        ).model_dump(by_alias=True),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 提取第一条错误信息作为 message
    msg = "Invalid request parameter"
    if exc.errors():
        e = exc.errors()[0]
        loc = ".".join(str(x) for x in e.get("loc", []))
        msg = f"{loc}: {e.get('msg', msg)}"
    return JSONResponse(
        status_code=400,
        content=ApiResponse(
            code=BizCode.PARAM_INVALID,
            message=msg,
            data=None,
            timestamp=_now_ms(),
            requestId=_new_request_id(),
        ).model_dump(by_alias=True),
    )


async def http_exception_handler(request: Request, exc):
    """统一处理 FastAPI HTTPException"""
    from starlette.exceptions import HTTPException as StarletteHTTPException
    if isinstance(exc, StarletteHTTPException):
        code_map = {401: BizCode.UNAUTHORIZED, 404: BizCode.NOT_FOUND, 409: BizCode.CONFLICT}
        bcode = code_map.get(exc.status_code, exc.status_code)
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiResponse(
                code=bcode,
                message=str(exc.detail),
                data=None,
                timestamp=_now_ms(),
                requestId=_new_request_id(),
            ).model_dump(by_alias=True),
        )
    raise exc


async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ApiResponse(
            code=BizCode.SYSTEM_ERROR,
            message="Internal Server Error",
            data=None,
            timestamp=_now_ms(),
            requestId=_new_request_id(),
        ).model_dump(by_alias=True),
    )


def _now_ms() -> int:
    from datetime import datetime, timezone
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(BizException, biz_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
