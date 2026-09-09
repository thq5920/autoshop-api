"""SQLAlchemy 数据库引擎与 Session。

设计原则:
    * init_db()  仅按 Model 建表("CREATE TABLE IF NOT EXISTS")，
                 不修改已存在表结构、不清数据、不跑迁移。
    * 清空/灌入数据 -> app.test_data.reset_test_data()。
    * 历史外键迁移 -> scripts.migrate_database (独立脚本)。
    * 本模块不含 SET FOREIGN_KEY_CHECKS。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _import_models():
    from app.models import user, product, cart, order  # noqa: F401


def init_db():
    """按 Model 建表。已存在则不动。重复启动幂等。"""
    _import_models()
    Base.metadata.create_all(bind=engine)
