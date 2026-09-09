"""
api_tests/common/db_manager.py
==============================
测试数据库管理：仅作为 app.test_data.reset_test_data() 的薄壳包装，
禁止再自行解析 INSERT VALUES 或产生新的 reset/seed 实现。

CLI:
    python -m api_tests.common.db_manager reset
    python -m api_tests.common.db_manager validate
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

# 将项目根加入 import path
_project_root = Path(__file__).resolve().parents[2]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from sqlalchemy import func, select

from app.database import SessionLocal, engine
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.test_data import reset_test_data as _reset_test_data


def reset_test_data() -> None:
    """重置测试数据：清空 + 重新灌入固定 mock 数据。

    委托给 app.test_data.reset_test_data()，唯一实现入口。
    """
    _reset_test_data()


class DataIntegrityError(AssertionError):
    """mock 数据完整性校验失败。"""
    pass


def validate_data_integrity() -> None:
    """校验 mock 数据的逻辑关联完整性（替代物理 FK）。

    1. cart_items.user_id    -> users.id
    2. cart_items.product_id -> products.id
    3. orders.user_id        -> users.id
    4. order_items.order_id  -> orders.id
    5. order_items.product_id -> products.id
    6. order_items.amount    == quantity * unit_price（Decimal 精度）
    7. orders.total_amount   == SUM(order_items.amount)（Decimal 精度）

    失败抛 DataIntegrityError。
    """
    db = SessionLocal()
    try:
        # 1. cart_items.user_id -> users.id
        n = db.execute(
            select(func.count(CartItem.id))
            .where(~select(User.id).where(User.id == CartItem.user_id).exists())
        ).scalar_one()
        if n:
            raise DataIntegrityError(f"orphan cart_items.user_id: {n}")

        # 2. cart_items.product_id -> products.id
        n = db.execute(
            select(func.count(CartItem.id))
            .where(~select(Product.id).where(Product.id == CartItem.product_id).exists())
        ).scalar_one()
        if n:
            raise DataIntegrityError(f"orphan cart_items.product_id: {n}")

        # 3. orders.user_id -> users.id
        n = db.execute(
            select(func.count(Order.id))
            .where(~select(User.id).where(User.id == Order.user_id).exists())
        ).scalar_one()
        if n:
            raise DataIntegrityError(f"orphan orders.user_id: {n}")

        # 4. order_items.order_id -> orders.id
        n = db.execute(
            select(func.count(OrderItem.id))
            .where(~select(Order.id).where(Order.id == OrderItem.order_id).exists())
        ).scalar_one()
        if n:
            raise DataIntegrityError(f"orphan order_items.order_id: {n}")

        # 5. order_items.product_id -> products.id
        n = db.execute(
            select(func.count(OrderItem.id))
            .where(~select(Product.id).where(Product.id == OrderItem.product_id).exists())
        ).scalar_one()
        if n:
            raise DataIntegrityError(f"orphan order_items.product_id: {n}")

        # 6. order_items.amount == quantity * unit_price
        rows = db.execute(
            select(
                OrderItem.id,
                OrderItem.amount,
                OrderItem.quantity,
                OrderItem.unit_price,
            )
        ).all()
        for oid, amt, q, u in rows:
            if Decimal(str(amt)) != Decimal(str(q)) * Decimal(str(u)):
                raise DataIntegrityError(
                    f"order_items.id={oid} amount={amt} != quantity({q}) * unit_price({u})"
                )

        # 7. orders.total_amount == SUM(order_items.amount)
        rows = db.execute(
            select(
                Order.id,
                Order.total_amount,
                select(func.coalesce(func.sum(OrderItem.amount), 0))
                .where(OrderItem.order_id == Order.id)
                .scalar_subquery(),
            )
        ).all()
        for oid, total, item_total in rows:
            if Decimal(str(total)) != Decimal(str(item_total)):
                raise DataIntegrityError(
                    f"orders.id={oid} total_amount={total} != sum(items)={item_total}"
                )
    finally:
        db.close()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "reset"
    if cmd == "reset":
        reset_test_data()
    elif cmd == "validate":
        validate_data_integrity()
    else:
        raise SystemExit(f"unknown cmd: {cmd}")
    print(f"[db_manager] {cmd} done")
