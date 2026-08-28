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
    nickname: Optional[str] = Field(default=None, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=120)

    @field_validator("phone")
    @classmethod
    def _v_phone(cls, v):
        if v is None or v == "":
            return None
        if not (v.isdigit() and len(v) == 11):
            raise ValueError("phone must be 11 digits")
        return v


class UpdateMeData(BaseModel):
    userId: int
    nickname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
