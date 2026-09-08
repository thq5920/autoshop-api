"""测试用内部接口(仅当 DEBUG=true 时启用)"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, reset_db
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.response import ok
from app.security import hash_password

router = APIRouter(prefix="/_test", tags=["test-only"])

# 商品种子数据
PRODUCT_SEEDS = [
    {"id": 1001, "name": "iPhone 17",            "category": "phone",    "price": 5999.00, "stock": 100, "status": "ON_SALE"},
    {"id": 1002, "name": "MacBook Air",          "category": "computer", "price": 7999.00, "stock": 50,  "status": "ON_SALE"},
    {"id": 1003, "name": "AirPods",              "category": "audio",   "price": 999.00,  "stock": 0,   "status": "ON_SALE"},
    {"id": 1004, "name": "Test Offline Product", "category": "test",    "price": 100.00, "stock": 10,  "status": "OFF_SHELF"},
]


@router.post("/reset", response_model=None)
def reset(db: Session = Depends(get_db)):
    """重置数据库：清空所有表数据 + 重建表结构（无外键） + 恢复种子数据。
    仅供自动化测试用，DEBUG=false 时禁用。
    """
    if not settings.DEBUG:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="disabled in production")

    # 1. 重置表结构（无外键）
    reset_db()

    # 2. 恢复商品种子（所有 AUTO_INCREMENT 从初始值开始）
    for seed in PRODUCT_SEEDS:
        db.add(Product(**seed, description="AutoShop Test Product"))

    # 3. 恢复 demo 用户
    db.add(User(
        username="demo",
        password_hash=hash_password("Demo@123456"),
        email="demo@example.com",
        phone="13800138000",
        nickname="演示用户",
    ))

    db.commit()
    return ok(data={"resetAt": int(datetime.now(timezone.utc).timestamp() * 1000)})
