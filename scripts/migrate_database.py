#!/usr/bin/env python3
"""
scripts/migrate_database.py
============================
数据库迁移脚本：将历史 MySQL 物理外键全部删除，并为所有逻辑关联字段补齐普通索引。

行为:
    1. 查询 information_schema.KEY_COLUMN_USAGE，删除所有 REFERENCED_TABLE_NAME IS NOT NULL 的约束。
    2. 检查并创建所有逻辑关联字段的普通索引（如果不存在）。
    3. 可重复执行（幂等）。
    4. 最终 Physical Foreign Keys = 0。

输出示例:
    === Phase 1: Remove Foreign Keys ===
    Discovered 5 foreign keys:
      - cart_items.user_id -> users.id (constraint: cart_items_ibfk_1)
      ...
    Removed foreign keys: 5
    Remaining foreign keys: 0

    === Phase 2: Ensure Logic FK Indexes ===
    ix_cart_product_id ... OK (already exists)
    ix_orders_user_id   ... OK (already exists)
    ix_order_items_product_id ... created
    All required indexes present.

使用:
    python scripts/migrate_database.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# 将项目根加入 import path（允许直接 python scripts/xxx.py 运行）
_project_root = Path(__file__).resolve().parents[1]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from sqlalchemy import create_engine, text

from app.config import settings

# 需要保证存在的逻辑关联索引：{(table, column): index_name}
REQUIRED_INDEXES = {
    ("cart_items",  "user_id"):    "ix_cart_user_id",
    ("cart_items",  "product_id"): "ix_cart_product_id",
    ("orders",      "user_id"):    "ix_orders_user_id",
    ("order_items", "order_id"):   "ix_order_items_order_id",
    ("order_items", "product_id"): "ix_order_items_product_id",
}


def list_fks(conn) -> list[dict]:
    return [
        dict(r)
        for r in conn.execute(
            text(
                """
                SELECT TABLE_NAME, CONSTRAINT_NAME, COLUMN_NAME,
                       REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE()
                  AND REFERENCED_TABLE_NAME IS NOT NULL
                ORDER BY TABLE_NAME, CONSTRAINT_NAME
                """
            )
        ).mappings().all()
    ]


def count_remaining_fks(conn) -> int:
    return conn.execute(
        text(
            """
            SELECT COUNT(*) FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = DATABASE()
              AND REFERENCED_TABLE_NAME IS NOT NULL
            """
        )
    ).scalar_one()


def index_exists(conn, table: str, index_name: str) -> bool:
    n = conn.execute(
        text(
            """
            SELECT COUNT(*) FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND INDEX_NAME = :idx
            """
        ),
        {"table": table, "idx": index_name},
    ).scalar_one()
    return n > 0


def create_index(conn, table: str, column: str, index_name: str) -> None:
    conn.execute(
        text(f"CREATE INDEX `{index_name}` ON `{table}` (`{column}`)")
    )


def main() -> int:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, future=True)

    print("=== Phase 1: Remove Foreign Keys ===")
    with engine.begin() as conn:
        fks = list_fks(conn)
        if not fks:
            print("No foreign keys found. Nothing to remove.")
        else:
            print(f"Discovered {len(fks)} foreign keys:")
            for fk in fks:
                print(
                    f"  - {fk['TABLE_NAME']}.{fk['COLUMN_NAME']} "
                    f"-> {fk['REFERENCED_TABLE_NAME']}.{fk['REFERENCED_COLUMN_NAME']} "
                    f"(constraint: {fk['CONSTRAINT_NAME']})"
                )
            for fk in fks:
                conn.execute(
                    text(
                        f"ALTER TABLE `{fk['TABLE_NAME']}` "
                        f"DROP FOREIGN KEY `{fk['CONSTRAINT_NAME']}`"
                    )
                )
                print(f"  dropped {fk['TABLE_NAME']}.{fk['CONSTRAINT_NAME']}")

        remaining = count_remaining_fks(conn)
        print(f"\nRemoved foreign keys: {len(fks)}")
        print(f"Remaining foreign keys: {remaining}")

        if remaining != 0:
            print("ERROR: Some foreign keys could not be removed. Aborting Phase 2.")
            return 1

    print("\n=== Phase 2: Ensure Logic FK Indexes ===")
    with engine.begin() as conn:
        for (table, column), index_name in REQUIRED_INDEXES.items():
            if index_exists(conn, table, index_name):
                print(f"  {index_name:35s} ... OK (already exists)")
            else:
                print(f"  {index_name:35s} ... creating ...")
                create_index(conn, table, column, index_name)
                print(f"  {index_name:35s} ... created")
        print("\nAll required indexes present.")

    print("\n=== Migration Complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
