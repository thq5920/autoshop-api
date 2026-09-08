"""SQLAlchemy 数据库引擎与 Session"""
from sqlalchemy import create_engine, text
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


def _import_models():
    """导入所有模型以注册到 Base.metadata（无任何外键定义）"""
    from app.models import user, product, cart, order  # noqa: F401


def init_db():
    """建表(由 main.py / seed.py 调用)。
    通过 SQLAlchemy Model 建表，不会生成任何 FOREIGN KEY。
    """
    _import_models()
    Base.metadata.create_all(bind=engine)


def reset_db():
    """一次性重置所有表：DROP 全部表 + 重新 CREATE（无外键，带中文注释）。
    不做备份，不保留任何数据。
    依赖 SQLAlchemy Model 中的 __table_args__ / comment 定义。
    """
    _import_models()
    # 关闭外键检查，按依赖逆序 DROP
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f"DROP TABLE IF EXISTS `{table.name}`"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        # 重新建表（Model 中已无 ForeignKey，create_all 不会生成外键）
        Base.metadata.create_all(bind=engine)
    print("[reset_db] all tables dropped and recreated (no foreign keys).")
