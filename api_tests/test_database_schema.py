"""数据库层面的不变量测试。

    1. autoshop 数据库物理外键数量 == 0
    2. 所有逻辑关联字段存在
    3. mock 数据无孤儿记录
    4. order_items 金额正确（Decimal 精度）
    5. orders 总金额正确（Decimal 精度）

仅对真实 MySQL 库断言；需要先执行 migrate_database.py,
并且必须存在 mock 数据（脚本或测试 reset 均可）。
"""
from __future__ import annotations

from decimal import Decimal

import pytest
from sqlalchemy import select, text

from api_tests.common.db_manager import (
    reset_test_data,
    validate_data_integrity,
)
from app.database import SessionLocal, engine


REQUIRED_INDEXES = {
    ("cart_items",  "user_id"):    "ix_cart_user_id",
    ("cart_items",  "product_id"): "ix_cart_product_id",
    ("orders",      "user_id"):    "ix_orders_user_id",
    ("order_items", "order_id"):   "ix_order_items_order_id",
    ("order_items", "product_id"): "ix_order_items_product_id",
}


@pytest.fixture(scope="module", autouse=True)
def _prepare_db():
    """确保有数据可用于完整性检查。"""
    reset_test_data()
    yield


def test_no_physical_foreign_keys():
    with engine.connect() as conn:
        n = conn.execute(
            text(
                "SELECT COUNT(*) FROM information_schema.KEY_COLUMN_USAGE "
                "WHERE TABLE_SCHEMA = DATABASE() "
                "  AND REFERENCED_TABLE_NAME IS NOT NULL"
            )
        ).scalar_one()
    assert n == 0, f"expected 0 physical FK, got {n}"


@pytest.mark.parametrize(
    "table,column,index",
    [
        ("cart_items",  "user_id",    "ix_cart_user_id"),
        ("cart_items",  "product_id", "ix_cart_product_id"),
        ("orders",      "user_id",    "ix_orders_user_id"),
        ("order_items", "order_id",   "ix_order_items_order_id"),
        ("order_items", "product_id", "ix_order_items_product_id"),
    ],
)
def test_logic_fk_columns_and_index(table, column, index):
    with engine.connect() as conn:
        col = conn.execute(
            text(
                "SELECT 1 FROM information_schema.COLUMNS "
                "WHERE TABLE_SCHEMA = DATABASE() "
                "  AND TABLE_NAME = :t AND COLUMN_NAME = :c"
            ),
            {"t": table, "c": column},
        ).scalar_one_or_none()
        idx = conn.execute(
            text(
                "SELECT 1 FROM information_schema.STATISTICS "
                "WHERE TABLE_SCHEMA = DATABASE() "
                "  AND TABLE_NAME = :t AND INDEX_NAME = :i"
            ),
            {"t": table, "i": index},
        ).scalar_one_or_none()
    assert col == 1, f"missing column {table}.{column}"
    assert idx == 1, f"missing index {index} on {table}.{column}"


def test_no_orphan_records():
    """调用 db_manager.validate_data_integrity() 校验 7 项。"""
    validate_data_integrity()


def test_order_items_amount_correct_decimal():
    """order_items.amount == quantity * unit_price，统一使用 Decimal。"""
    from app.models.order import OrderItem
    db = SessionLocal()
    try:
        rows = db.execute(
            select(
                OrderItem.id,
                OrderItem.amount,
                OrderItem.quantity,
                OrderItem.unit_price,
            )
        ).all()
        assert rows, "no order_items"
        for oid, amt, q, u in rows:
            expected = Decimal(str(q)) * Decimal(str(u))
            actual = Decimal(str(amt))
            assert actual == expected, (
                f"order_items.id={oid}: amount={actual} != {q}*{u}={expected}"
            )
    finally:
        db.close()


def test_orders_total_amount_correct_decimal():
    """orders.total_amount == SUM(order_items.amount)，统一使用 Decimal。"""
    from app.models.order import Order, OrderItem
    from sqlalchemy import func
    db = SessionLocal()
    try:
        rows = db.execute(
            select(
                Order.id,
                Order.total_amount,
                select(func.coalesce(func.sum(OrderItem.amount), 0))
                .where(OrderItem.order_id == Order.id)
                .scalar_subquery(),
            )
        ).all()
        assert rows, "no orders"
        for oid, total, item_total in rows:
            assert Decimal(str(total)) == Decimal(str(item_total)), (
                f"orders.id={oid}: total_amount={total} != sum(items)={item_total}"
            )
    finally:
        db.close()
