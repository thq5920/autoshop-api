"""用户服务"""
from sqlalchemy.orm import Session

from app.config import settings
from app.exceptions import BizCode, BizException
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.security import hash_password, verify_password


def create_user(db: Session, req: RegisterRequest) -> User:
    if db.query(User).filter(User.username == req.username).first():
        raise BizException(BizCode.USERNAME_ALREADY_EXISTS, http_status=409)
    if db.query(User).filter(User.email == req.email).first():
        raise BizException(BizCode.EMAIL_ALREADY_EXISTS, http_status=409)

    user = User(
        username=req.username,
        password_hash=hash_password(req.password),
        email=req.email,
        phone=req.phone,
        nickname=req.username,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, username: str, password: str) -> User:
    """用户登录认证

    - settings.EXPOSE_AUTH_DETAIL = True (默认 / 测试场景):
        账号不存在 → 40301 ACCOUNT_NOT_EXISTS
        密码错误   → 40302 PASSWORD_INCORRECT
    - settings.EXPOSE_AUTH_DETAIL = False (生产):
        一律 → 40303 USERNAME_OR_PASSWORD_ERROR(防账号枚举)
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        if settings.EXPOSE_AUTH_DETAIL:
            raise BizException(BizCode.ACCOUNT_NOT_EXISTS, http_status=401)
        raise BizException(BizCode.USERNAME_OR_PASSWORD_ERROR, http_status=401)

    if not verify_password(password, user.password_hash):
        if settings.EXPOSE_AUTH_DETAIL:
            raise BizException(BizCode.PASSWORD_INCORRECT, http_status=401)
        raise BizException(BizCode.USERNAME_OR_PASSWORD_ERROR, http_status=401)

    return user
