"""SQLAlchemy 数据库引擎与 Session"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,    # MySQL 空闲断开保活
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db():
    """FastAPI 依赖:提供一个 Session,自动关闭"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """建表(由 main.py / seed.py 调用)"""
    # 导入所有模型以注册到 Base
    from app.models import user, product, cart, order  # noqa: F401
    Base.metadata.create_all(bind=engine)
