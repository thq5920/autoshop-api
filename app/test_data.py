"""测试数据管理。

唯一的 reset_test_data() 实现。
所有调用方（/_test/reset 接口、api_tests/common/db_manager.py）都引用本模块。

实现方式:
    通过 pymysql 直接执行 scripts/mock_data.sql 文本，
    不自行解析 INSERT VALUES，不依赖 SQLAlchemy ORM。
    这样可以完整支持 mysql CLI 的所有语义（包括 TRUNCATE 多表）。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# 将项目根加入 import path
_project_root = Path(__file__).resolve().parents[1]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from app.config import settings


MOCK_SQL_PATH = Path(__file__).resolve().parents[1] / "scripts" / "mock_data.sql"


def _mysql_execute(sql_text: str) -> None:
    """通过 subprocess 调用 mysql CLI 执行 SQL 文本。

    直接使用 mysql 而非 pymysql，是为了完整支持 TRUNCATE 的语义
    （MySQL TRUNCATE 不受 SET FOREIGN_KEY_CHECKS 影响）。
    """
    env = {
        "MYSQL_PWD": settings.MYSQL_PASSWORD,
    }
    result = subprocess.run(
        [
            "mysql",
            "-h", settings.MYSQL_HOST,
            "-P", str(settings.MYSQL_PORT),
            "-u", settings.MYSQL_USER,
            "--database", settings.MYSQL_DB,
            "--default-character-set=utf8mb4",
        ],
        input=sql_text.encode("utf-8"),
        env=env,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"mysql command failed (exit {result.returncode}):\n"
            f"stderr: {result.stderr.decode(errors='replace')}"
        )


def reset_test_data() -> None:
    """完整重置测试数据：清空 + 重新灌入固定 mock 数据。

    等价于 `mysql ... < scripts/mock_data.sql`。
    """
    if not MOCK_SQL_PATH.exists():
        raise FileNotFoundError(f"mock_data.sql not found at {MOCK_SQL_PATH}")
    sql_text = MOCK_SQL_PATH.read_text(encoding="utf-8")
    _mysql_execute(sql_text)


if __name__ == "__main__":
    reset_test_data()
    print("[reset_test_data] done")
