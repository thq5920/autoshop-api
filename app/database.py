"""SQLAlchemy 数据库引擎与 Session。

设计原则:
- 数据库层不持有 DROP TABLE / 重建表的能力。
- 初始化只负责"按 Model 建表"(`init_db`),已存在的表不会被改动。
- 测试重置只清空数据(`clear_test_data`),保留表结构与外键策略。
- 本项目不使用 MySQL FOREIGN KEY (由业务代码保证关联完整性),
  所有 TRUNCATE 可按任意顺序,但保留一个固定顺序以方便排错与日志比对。
"""
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
    """导入所有模型以注册到 Base.metadata(无任何外键定义)"""
    from app.models import user, product, cart, order  # noqa: F401


# 测试数据清空顺序。
# 顺序按依赖反向排(虽然无 FK 但写代码保持一致便于审计),
# 同时也会被 SQL 脚本 / README 引用,如有调整请同步。
_TRUNCATE_ORDER = (
    "order_items",
    "orders",
    "cart_items",
    "products",
    "users",
)


def init_db():
    """创建不存在的表(由 main.py 启动时调用)。

    - 只会 `CREATE TABLE IF NOT EXISTS`,已存在的表及其数据不会被改动;
    - 由 SQLAlchemy Model 的 `Column` 定义建表,不会生成 FOREIGN KEY;
    - 重复启动幂等。
    """
    _import_models()
    Base.metadata.create_all(bind=engine)


def clear_test_data():
    """清空测试数据但保留表结构。

    - MySQL (项目目标方言): 使用 `TRUNCATE TABLE`,并通过 SET FOREIGN_KEY_CHECKS
      兼容可能存在的历史 FK;TRUNCATE 同时重置 AUTO_INCREMENT。
    - 其他方言 (例如 SQLite 用于本地集成测试): 回退为 `DELETE FROM`,
      效果等价于"清空数据,保留表结构"。
    - 按 `_TRUNCATE_ORDER` 逆依赖顺序执行,与 README 描述保持一致。
    """
    use_truncate = engine.dialect.name in ("mysql", "mariadb")
    fk_off_sql = "SET FOREIGN_KEY_CHECKS = 0" if use_truncate else None
    fk_on_sql = "SET FOREIGN_KEY_CHECKS = 1" if use_truncate else None

    with engine.begin() as conn:
        if fk_off_sql is not None:
            conn.execute(text(fk_off_sql))
        try:
            for table in _TRUNCATE_ORDER:
                if use_truncate:
                    conn.execute(text(f"TRUNCATE TABLE `{table}`"))
                else:
                    conn.execute(text(f"DELETE FROM `{table}`"))
        finally:
            if fk_on_sql is not None:
                conn.execute(text(fk_on_sql))
