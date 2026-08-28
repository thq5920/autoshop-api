"""测试用内部接口(仅当 DEBUG=true 时启用)"""
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.response import ok

router = APIRouter(prefix="/_test", tags=["test-only"])

# 商品种子数据(用于 _test/reset 时重置库存)
PRODUCT_SEEDS = [
    {"id": 1001, "name": "iPhone 17", "category": "phone",    "price": 5999.00, "stock": 100, "status": "ON_SALE"},
    {"id": 1002, "name": "MacBook Air","category": "computer", "price": 7999.00, "stock": 50,  "status": "ON_SALE"},
    {"id": 1003, "name": "AirPods",    "category": "audio",    "price": 999.00,  "stock": 0,   "status": "ON_SALE"},
    {"id": 1004, "name": "Test Offline Product", "category": "test", "price": 100.00, "stock": 10, "status": "OFF_SHELF"},
]


@router.post("/reset", response_model=None)
def reset(db: Session = Depends(get_db)):
    """重置商品库存 + 清空所有订单/购物车。仅供自动化测试用,生产应禁用。"""
    if not settings.DEBUG:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="disabled in production")

    # 清订单/购物车
    db.query(OrderItem).delete()
    db.query(Order).delete()
    db.query(CartItem).delete()

    # 重置商品
    for seed in PRODUCT_SEEDS:
        p = db.get(Product, seed["id"])
        if p:
            p.stock = seed["stock"]
            p.status = seed["status"]
            p.price = seed["price"]
            p.name = seed["name"]
            p.category = seed["category"]
        else:
            db.add(Product(**seed, description="AutoShop Test Product"))
    db.commit()
    return ok(data={"resetAt": int(datetime.utcnow().timestamp() * 1000)})
