"""用户模型"""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"
    __table_args__ = {"mysql_comment": "用户表"}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(20), unique=True, nullable=False, index=True, comment="登录用户名")
    password_hash = Column(String(128), nullable=False, comment="登录密码哈希值")
    email = Column(String(120), unique=True, nullable=False, index=True, comment="用户邮箱")
    phone = Column(String(20), nullable=True, comment="手机号")
    nickname = Column(String(50), nullable=True, comment="用户昵称")
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="创建时间",
    )
