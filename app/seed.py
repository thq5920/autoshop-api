"""种子数据管理。

对外职责划分:
    * seed_db()       启动时调用：按固定 ID / 唯一字段逐条判断，缺失则补充；
                       不删除已有业务数据，适用于"上线"后首次或重复启动。
    * 测试数据重置 -> app.test_data.reset_test_data()（通过 mysql 执行 scripts/mock_data.sql）。
    * clear_test_data / seed_test_data / reset_test_data 已移至 app.test_data，
      本模块不再负责。

固定商品数据（仅用于 seed_db 补充，与 mock_data.sql 不同）:
    1001 iPhone 17              price=5999.00 stock=100 status=ON_SALE
    1002 MacBook Air            price=7999.00 stock=50  status=ON_SALE
    1003 AirPods                price=999.00  stock=0   status=ON_SALE
    1004 Test Offline Product   price=100.00  stock=10  status=OFF_SHELF

固定测试用户:
    username: demo
    password: Demo@123456
"""
from sqlalchemy import select

from app.database import SessionLocal, init_db
from app.models.product import Product
from app.models.user import User
from app.security import hash_password


PRODUCTS = [
    dict(id=1001, name="iPhone 17",            category="phone",    price=5999.00, stock=100, status="ON_SALE"),
    dict(id=1002, name="MacBook Air",            category="computer", price=7999.00, stock=50,  status="ON_SALE"),
    dict(id=1003, name="AirPods",                category="audio",    price=999.00,  stock=0,   status="ON_SALE"),
    dict(id=1004, name="Test Offline Product",   category="test",     price=100.00, stock=10,  status="OFF_SHELF"),
]


DEMO_USERNAME = "demo"
DEMO_PASSWORD = "Demo@123456"
DEMO_EMAIL = "demo@example.com"
DEMO_PHONE = "13800138000"
DEMO_NICKNAME = "演示用户"


def _build_demo_user() -> User:
    return User(
        username=DEMO_USERNAME,
        password_hash=hash_password(DEMO_PASSWORD),
        email=DEMO_EMAIL,
        phone=DEMO_PHONE,
        nickname=DEMO_NICKNAME,
    )


def seed_db() -> None:
    """补充基础 Seed 数据。

    - 按固定 `Product.id` 逐条 `db.get()` 判断，缺失则插入；
    - 用户使用唯一字段 `username='demo'` 判断；
    - 不会删除已有业务数据，不会重置 AUTO_INCREMENT；
    - 重复启动幂等。
    """
    db = SessionLocal()
    try:
        inserted_products = 0
        for p in PRODUCTS:
            if db.get(Product, p["id"]) is None:
                db.add(Product(**p, description="AutoShop Test Product"))
                inserted_products += 1

        demo_exists = db.execute(
            select(User).where(User.username == DEMO_USERNAME)
        ).scalar_one_or_none() is not None
        if not demo_exists:
            db.add(_build_demo_user())

        db.commit()
        if inserted_products:
            print(f"[seed_db] inserted {inserted_products} missing products")
        if not demo_exists:
            print("[seed_db] inserted demo user")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_db()
    print("Seed done.")
