"""业务异常 + 统一异常处理

- BizCode:五位制业务码表(详见 README / app/i18n.py)
- BizException:抛出后被 biz_exception_handler 捕获,message 按 locale 自动从 i18n 表取
- validation_exception_handler:Pydantic 校验失败 → HTTP 422 + 具体业务码(通过哨兵映射)
"""
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import i18n
from app.response import ApiResponse


class BizException(Exception):
    """业务异常:code 为业务码,http_status 为 HTTP 状态码

    使用示例:
        raise BizException(BizCode.PASSWORD_INCORRECT)         # message 自动按 locale 取
        raise BizException(BizCode.INTERNAL, "自定义消息")       # 自定义 message
        raise BizException(BizCode.NOT_FOUND, http_status=404)
    """

    def __init__(
        self,
        code: int,
        message: str = "",
        http_status: int | None = None,
    ):
        self.code = code
        self._explicit_message = message
        # 未传 http_status 时按 BizCode._http_status_map 自动推断
        self.http_status = (
            http_status
            if http_status is not None
            else BizCode._http_status_map.get(code, 400)
        )

    def resolve_message(self, locale: str) -> str:
        """按 locale 解析最终 message:优先显式传入,否则查 i18n 表"""
        if self._explicit_message:
            return self._explicit_message
        return i18n.msg(self.code, locale)


# ============ 业务码常量(五位制:第 1 位=大类,2-3 位=模块,4-5 位=序号) ============
class BizCode:
    SUCCESS = 200                              # 成功

    # 通用 (400xx)
    PARAM_INVALID = 40001                      # 参数格式错误
    PARAM_MISSING = 40002                      # 必填参数缺失
    PARAM_OUT_OF_RANGE = 40003                 # 参数超出允许范围

    # 认证 (401xx)
    UNAUTHORIZED = 40101                       # 未登录或登录已失效
    TOKEN_INVALID = 40102                      # 登录凭证无效
    TOKEN_EXPIRED = 40103                      # 登录凭证已过期
    PERMISSION_DENIED = 40104                  # 无权访问该资源
    ACCOUNT_DISABLED = 40105                   # 账号已被禁用

    # 账号密码格式 (402xx) — Pydantic 校验后映射 → HTTP 422
    USERNAME_FORMAT_ERROR = 40201              # 用户名格式不正确
    USERNAME_TOO_SHORT = 40202                 # 用户名过短
    USERNAME_TOO_LONG = 40203                  # 用户名过长
    PASSWORD_FORMAT_ERROR = 40204              # 密码格式不正确
    PASSWORD_TOO_SHORT = 40205                 # 密码过短
    PASSWORD_TOO_LONG = 40206                  # 密码过长
    EMAIL_FORMAT_ERROR = 40207                 # 邮箱格式不正确
    EMAIL_TOO_LONG = 40208                     # 邮箱过长
    PHONE_FORMAT_ERROR = 40209                 # 手机号格式不正确
    NICKNAME_TOO_LONG = 40210                  # 昵称过长

    # 注册/登录业务 (403xx) → HTTP 401
    ACCOUNT_NOT_EXISTS = 40301                  # 账号不存在(DEBUG 暴露)
    PASSWORD_INCORRECT = 40302                 # 密码错误(DEBUG 暴露)
    USERNAME_OR_PASSWORD_ERROR = 40303         # 用户名或密码错误(默认对外)

    # 用户资料 (404xx)
    USER_NOT_FOUND = 40401                     # 用户不存在
    NO_UPDATE_FIELDS = 40402                   # 资料无任何更新

    # 商品 (405xx)
    PRODUCT_NOT_FOUND = 40501                  # 商品不存在
    PRODUCT_OFF_SHELF = 40502                  # 商品已下架
    INSUFFICIENT_STOCK = 40503                 # 库存不足
    QUANTITY_INVALID = 40504                   # 购买数量不合法

    # 购物车 (406xx)
    CART_ITEM_NOT_FOUND = 40601                # 购物车项不存在
    CART_EMPTY = 40602                         # 购物车为空

    # 订单 (407xx)
    ORDER_NOT_FOUND = 40701                    # 订单不存在
    ORDER_STATUS_INVALID = 40702               # 订单状态不允许此操作
    PAY_FAILED = 40703                         # 支付失败

    # 冲突 (409xx) → HTTP 409
    USERNAME_ALREADY_EXISTS = 40901            # 用户名已被占用
    EMAIL_ALREADY_EXISTS = 40902               # 邮箱已被注册
    PHONE_ALREADY_EXISTS = 40903               # 手机号已被注册

    # 系统 (5xxxx) → HTTP 500 / 503
    SYSTEM_ERROR = 50001                       # 系统繁忙
    DATABASE_ERROR = 50002                     # 数据库异常
    SERVICE_UNAVAILABLE = 50301                # 服务暂不可用

    # HTTP status 映射表(码值 → HTTP 状态码)
    # 仅用于 BizException 默认推断;调用处显式传 http_status 时以显式值为准
    _http_status_map: dict[int, int] = {
        # 通用
        40001: 422, 40002: 400, 40003: 400,
        # 认证
        40101: 401, 40102: 401, 40103: 401, 40104: 403, 40105: 403,
        # 格式校验 → 422
        40201: 422, 40202: 422, 40203: 422, 40204: 422, 40205: 422,
        40206: 422, 40207: 422, 40208: 422, 40209: 422, 40210: 422,
        # 登录业务 → 401
        40301: 401, 40302: 401, 40303: 401,
        # 用户资料
        40401: 404, 40402: 400,
        # 商品
        40501: 404, 40502: 400, 40503: 400, 40504: 400,
        # 购物车
        40601: 404, 40602: 400,
        # 订单
        40701: 404, 40702: 400, 40703: 400,
        # 冲突
        40901: 409, 40902: 409, 40903: 409,
        # 系统
        50001: 500, 50002: 500, 50301: 503,
    }


# 已定义的业务码集合,用于 Pydantic 校验失败时的哨兵校验
_VALID_BIZ_CODES: set[int] = {
    v for k, v in vars(BizCode).items()
    if not k.startswith("_") and isinstance(v, int)
}


# ============ 工具函数 ============
def _new_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:16]}"


def _now_ms() -> int:
    from datetime import datetime, timezone
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def _resolve_locale(request: Request) -> str:
    """从 query 参数 / Accept-Language 头解析语言"""
    q_lang = request.query_params.get("lang") if hasattr(request, "query_params") else None
    return i18n.resolve_lang(
        request.headers.get("accept-language") if hasattr(request, "headers") else None,
        q_lang,
    )


def _envelope(code: int, message: str, locale: str) -> dict:
    return ApiResponse(
        code=code,
        message=message,
        data=None,
        timestamp=_now_ms(),
        requestId=_new_request_id(),
    ).model_dump(by_alias=True)


# ============ 异常处理器 ============
async def biz_exception_handler(request: Request, exc: BizException):
    locale = _resolve_locale(request)
    return JSONResponse(
        status_code=exc.http_status,
        content=_envelope(exc.code, exc.resolve_message(locale), locale),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Pydantic 校验失败 → HTTP 422

    schemas 用 `raise ValueError("40202")` 这种纯码字符串做哨兵,
    这里解析出来后映射到 BizCode;否则兜底为 PARAM_INVALID。
    """
    locale = _resolve_locale(request)
    bcode = BizCode.PARAM_INVALID
    if exc.errors():
        e = exc.errors()[0]
        raw_msg = (e.get("msg") or "").strip()
        # 处理 "Value error, 40202" 这种 Pydantic 自动加前缀的情况
        sentinel = raw_msg
        if sentinel.lower().startswith("value error, "):
            sentinel = sentinel[len("value error, "):].strip()
        if sentinel.isdigit():
            try:
                candidate = int(sentinel)
                if candidate in _VALID_BIZ_CODES:
                    bcode = candidate
            except ValueError:
                pass
    return JSONResponse(
        status_code=422,
        content=_envelope(bcode, i18n.msg(bcode, locale), locale),
    )


async def http_exception_handler(request: Request, exc):
    """统一处理 FastAPI HTTPException(主要是 401/403/404/409)"""
    from starlette.exceptions import HTTPException as StarletteHTTPException
    if isinstance(exc, StarletteHTTPException):
        locale = _resolve_locale(request)
        code_map = {
            401: BizCode.UNAUTHORIZED,
            403: BizCode.PERMISSION_DENIED,
            404: BizCode.PARAM_INVALID,
            409: BizCode.USERNAME_ALREADY_EXISTS,
        }
        bcode = code_map.get(exc.status_code, exc.status_code)
        message = str(exc.detail) if exc.detail else i18n.msg(bcode, locale)
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope(bcode, message, locale),
        )
    raise exc


async def unhandled_exception_handler(request: Request, exc: Exception):
    locale = _resolve_locale(request)
    return JSONResponse(
        status_code=500,
        content=_envelope(BizCode.SYSTEM_ERROR, i18n.msg(BizCode.SYSTEM_ERROR, locale), locale),
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(BizException, biz_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
