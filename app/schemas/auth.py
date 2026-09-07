"""认证相关 Schemas

校验失败时,ValueError 的 msg 直接传业务码字符串(如 "40202"),
由 app/exceptions.py 的 validation_exception_handler 解析后映射到具体 BizCode + HTTP 422。
"""
import re

from pydantic import BaseModel, EmailStr, Field, field_validator


USERNAME_RE = re.compile(r"^[A-Za-z0-9_]+$")
PHONE_RE = re.compile(r"^1[3-9]\d{9}$")


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone: str | None = None

    @field_validator("username")
    @classmethod
    def _v_username(cls, v: str) -> str:
        if len(v) < 4:
            raise ValueError("40202")          # USERNAME_TOO_SHORT
        if len(v) > 20:
            raise ValueError("40203")          # USERNAME_TOO_LONG
        if not USERNAME_RE.match(v):
            raise ValueError("40201")          # USERNAME_FORMAT_ERROR
        return v

    @field_validator("password")
    @classmethod
    def _v_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("40205")          # PASSWORD_TOO_SHORT
        if len(v) > 20:
            raise ValueError("40206")          # PASSWORD_TOO_LONG
        return v

    @field_validator("phone")
    @classmethod
    def _v_phone(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        if not PHONE_RE.match(v):
            raise ValueError("40209")          # PHONE_FORMAT_ERROR
        return v


class RegisterData(BaseModel):
    userId: int
    username: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginData(BaseModel):
    accessToken: str
    tokenType: str = "Bearer"
    expiresIn: int
    userId: int
