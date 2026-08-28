"""认证相关 Schemas"""
import re

from pydantic import BaseModel, EmailStr, Field, field_validator


USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{4,20}$")
PASSWORD_RE = re.compile(r"^.{8,20}$")
PHONE_RE = re.compile(r"^1[3-9]\d{9}$")


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone: str | None = None

    @field_validator("username")
    @classmethod
    def _v_username(cls, v: str) -> str:
        if not USERNAME_RE.match(v):
            raise ValueError("username must be 4-20 chars of letters/digits/underscore")
        return v

    @field_validator("password")
    @classmethod
    def _v_password(cls, v: str) -> str:
        if not PASSWORD_RE.match(v):
            raise ValueError("password must be 8-20 chars")
        return v

    @field_validator("phone")
    @classmethod
    def _v_phone(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        if not PHONE_RE.match(v):
            raise ValueError("phone must be a valid CN mobile number")
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
