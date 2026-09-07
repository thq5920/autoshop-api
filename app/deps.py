"""FastAPI 依赖注入:获取当前登录用户"""
from fastapi import Depends, Header
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import BizCode, BizException
from app.models.user import User
from app.security import decode_token


def get_current_user(
    authorization: str = Header(default=""),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise BizException(BizCode.UNAUTHORIZED, http_status=401)
    token = authorization[7:].strip()
    if not token:
        raise BizException(BizCode.UNAUTHORIZED, http_status=401)
    try:
        payload = decode_token(token)
    except ExpiredSignatureError:
        raise BizException(BizCode.TOKEN_EXPIRED, http_status=401)
    except InvalidTokenError:
        raise BizException(BizCode.TOKEN_INVALID, http_status=401)

    user_id = payload.get("user_id")
    if not user_id:
        raise BizException(BizCode.TOKEN_INVALID, http_status=401)

    user = db.get(User, user_id)
    if not user:
        raise BizException(BizCode.USER_NOT_FOUND, http_status=404)
    return user
