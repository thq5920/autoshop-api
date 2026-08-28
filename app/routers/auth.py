"""认证路由:注册 / 登录"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.response import ApiResponse, ok
from app.schemas.auth import LoginData, LoginRequest, RegisterData, RegisterRequest
from app.security import create_access_token
from app.services.user_service import authenticate, create_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    user = create_user(db, req)
    return ok(
        data=RegisterData(userId=user.id, username=user.username).model_dump(),
        request_id=f"req_register_{user.id}",
    )


@router.post("/login", response_model=ApiResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate(db, req.username, req.password)
    token = create_access_token(user.id)
    return ok(
        data=LoginData(
            accessToken=token,
            tokenType="Bearer",
            expiresIn=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            userId=user.id,
        ).model_dump(),
        request_id=f"req_login_{user.id}",
    )
