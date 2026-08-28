"""用户服务"""
from sqlalchemy.orm import Session

from app.exceptions import BizCode, BizException
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.security import hash_password, verify_password


def create_user(db: Session, req: RegisterRequest) -> User:
    if db.query(User).filter(User.username == req.username).first():
        raise BizException(BizCode.CONFLICT, "Username already exists", 409)
    if db.query(User).filter(User.email == req.email).first():
        raise BizException(BizCode.CONFLICT, "Email already exists", 409)

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
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise BizException(BizCode.UNAUTHORIZED, "Invalid username or password", 401)
    return user
