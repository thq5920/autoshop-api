"""用户中心 Schemas"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class MeData(BaseModel):
    userId: int
    username: str
    email: str
    phone: Optional[str] = None
    nickname: Optional[str] = None
    createdAt: datetime


class UpdateMeRequest(BaseModel):
    nickname: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)

    @field_validator("nickname")
    @classmethod
    def _v_nickname(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if len(v) > 50:
            raise ValueError("40210")          # NICKNAME_TOO_LONG
        return v

    @field_validator("phone")
    @classmethod
    def _v_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return None
        if not (v.isdigit() and len(v) == 11 and v.startswith("1")):
            raise ValueError("40209")          # PHONE_FORMAT_ERROR
        return v

    @field_validator("email")
    @classmethod
    def _v_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return None
        if len(v) > 120:
            raise ValueError("40208")          # EMAIL_TOO_LONG
        return v


class UpdateMeData(BaseModel):
    userId: int
    nickname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
