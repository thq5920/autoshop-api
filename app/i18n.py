"""多语言消息模块

- 支持 zh-CN / en-US
- 通过 Accept-Language header 或 ?lang= 查询参数切换
- 默认中文(zh-CN),便于接口自动化测试
"""
from typing import Optional


# 支持的语言 + 默认
SUPPORTED = ("zh-CN", "en-US")
DEFAULT = "zh-CN"


def parse_accept_language(header: Optional[str]) -> str:
    """解析 Accept-Language,返回最匹配的支持语言

    简化处理:
      1. 多个语言按 ',' 切,每个取 ';' 前的主标签
      2. 完全匹配优先( zh-CN / en-US )
      3. 否则按主标签前缀匹配( zh -> zh-CN, en -> en-US )
      4. 都没有则返回默认 zh-CN
    """
    if not header:
        return DEFAULT
    for raw_tag in header.split(","):
        tag = raw_tag.split(";")[0].strip()
        if not tag:
            continue
        if tag in SUPPORTED:
            return tag
        primary = tag.split("-")[0].lower()
        for s in SUPPORTED:
            if s.lower().startswith(primary + "-") or s.lower() == primary:
                return s
    return DEFAULT


def resolve_lang(accept_language: Optional[str], query_lang: Optional[str] = None) -> str:
    """优先用 query 参数 ?lang=,否则用 Accept-Language"""
    if query_lang and query_lang in SUPPORTED:
        return query_lang
    return parse_accept_language(accept_language)


# ============ 中文(zh-CN)消息表 ============
MESSAGES_ZH = {
    200:     "成功",
    40001:   "参数格式错误",
    40002:   "必填参数缺失",
    40003:   "参数超出允许范围",
    40101:   "未登录或登录已失效,请重新登录",
    40102:   "登录凭证无效",
    40103:   "登录凭证已过期,请重新登录",
    40104:   "无权访问该资源",
    40105:   "账号已被禁用",
    40201:   "用户名格式不正确,仅允许字母、数字、下划线",
    40202:   "用户名过短,至少需要 4 位",
    40203:   "用户名过长,最多 20 位",
    40204:   "密码格式不正确",
    40205:   "密码过短,至少需要 8 位",
    40206:   "密码过长,最多 20 位",
    40207:   "邮箱格式不正确",
    40208:   "邮箱过长,最多 120 位",
    40209:   "手机号格式不正确",
    40210:   "昵称过长,最多 50 位",
    40301:   "账号不存在",
    40302:   "密码错误",
    40303:   "用户名或密码错误",
    40401:   "用户不存在",
    40402:   "资料无任何更新",
    40501:   "商品不存在",
    40502:   "商品已下架",
    40503:   "库存不足",
    40504:   "购买数量必须为正整数,且不超过单次上限",
    40601:   "购物车项不存在",
    40602:   "购物车为空",
    40701:   "订单不存在",
    40702:   "订单状态不允许此操作",
    40703:   "支付失败",
    40901:   "用户名已被占用",
    40902:   "邮箱已被注册",
    40903:   "手机号已被注册",
    50001:   "系统繁忙,请稍后再试",
    50002:   "数据库异常",
    50301:   "服务暂不可用,请稍后再试",
}


# ============ 英文(en-US)消息表 ============
MESSAGES_EN = {
    200:     "success",
    40001:   "Invalid parameter format",
    40002:   "Required parameter missing",
    40003:   "Parameter out of allowed range",
    40101:   "Not logged in or session expired, please login again",
    40102:   "Invalid token",
    40103:   "Token expired, please login again",
    40104:   "Permission denied",
    40105:   "Account has been disabled",
    40201:   "Username format error, only letters/digits/underscore allowed",
    40202:   "Username too short, at least 4 characters",
    40203:   "Username too long, at most 20 characters",
    40204:   "Password format error",
    40205:   "Password too short, at least 8 characters",
    40206:   "Password too long, at most 20 characters",
    40207:   "Email format error",
    40208:   "Email too long, at most 120 characters",
    40209:   "Phone format error",
    40210:   "Nickname too long, at most 50 characters",
    40301:   "Account does not exist",
    40302:   "Incorrect password",
    40303:   "Invalid username or password",
    40401:   "User does not exist",
    40402:   "No fields to update",
    40501:   "Product does not exist",
    40502:   "Product is off shelf",
    40503:   "Insufficient stock",
    40504:   "Invalid quantity, must be a positive integer within the per-order limit",
    40601:   "Cart item does not exist",
    40602:   "Cart is empty",
    40701:   "Order does not exist",
    40702:   "Order status does not allow this operation",
    40703:   "Payment failed",
    40901:   "Username already taken",
    40902:   "Email already registered",
    40903:   "Phone already registered",
    50001:   "Internal server error, please try again later",
    50002:   "Database error",
    50301:   "Service temporarily unavailable",
}


_LOCALES = {
    "zh-CN": MESSAGES_ZH,
    "en-US": MESSAGES_EN,
}


def msg(code: int, locale: str = DEFAULT, default: Optional[str] = None) -> str:
    """按 locale 取 message,找不到回退 default 或中文表,最后回退 'Unknown error'"""
    table = _LOCALES.get(locale) or _LOCALES[DEFAULT]
    if code in table:
        return table[code]
    if default:
        return default
    return _LOCALES[DEFAULT].get(code, "未知错误 / Unknown error")
