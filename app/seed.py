"""种子数据管理。

对外职责划分:

- `seed_db()`      启动时调用:按固定 ID / 唯一字段逐条判断,缺失则补充;
                   不删除已有业务数据,适用于"上线"后首次或重复启动。
- `clear_test_data()` 在 `database.py` 里实现,只清空表数据不破坏结构。
- `seed_test_data()` 假定调用前表已空,强制灌入全部固定测试数据。
- `reset_test_data()` = `clear_test_data()` + `seed_test_data()`。
                   是 `POST /api/v1/_test/reset` 的唯一实现路径,不再使用 DROP TABLE。

固定商品数据:
    1001 iPhone 17              price=5999.00 stock=100 status=ON_SALE
    1002 MacBook Air            price=7999.00 stock=50  status=ON_SALE
    1003 AirPods                price=999.00  stock=0   status=ON_SALE
    1004 Test Offline Product   price=100.00  stock=10  status=OFF_SHELF

固定测试用户:
    username: demo
    password: Demo@123456
    密码哈希通过 `app.security.hash_password()` 实时生成,杜绝 SQL 中使用
    placeholder hash。
"""
from sqlalchemy import select

from app.database import SessionLocal, clear_test_data, init_db
from app.models.product import Product
from app.models.user import User
from app.security import hash_password


PRODUCTS = [
    dict(id=1001, name="iPhone 17",            category="phone",    price=5999.00, stock=100, status="ON_SALE"),
    dict(id=1002, name="MacBook Air",          category="computer", price=7999.00, stock=50,  status="ON_SALE"),
    dict(id=1003, name="AirPods",              category="audio",    price=999.00,  stock=0,   status="ON_SALE"),
    dict(id=1004, name="Test Offline Product", category="test",     price=100.00, stock=10,  status="OFF_SHELF"),
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

    - 按固定 `Product.id` 逐条 `db.get()` 判断,缺失则插入;
    - 用户使用唯一字段 `username='demo'` 判断;
    - 不会删除已有业务数据,不会重置 AUTO_INCREMENT;
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


def seed_test_data() -> None:
    """强制灌入全部固定测试数据(假定调用前表为空,由 `clear_test_data()` 保证)。

    同样使用真实 bcrypt 哈希,而非 placeholder。
    """
    db = SessionLocal()
    try:
        for p in PRODUCTS:
            db.add(Product(**p, description="AutoShop Test Product"))
        db.add(_build_demo_user())
        db.commit()
    finally:
        db.close()


def reset_test_data() -> None:
    """测试环境重置数据:清空 + 重灌。

    - 等价于 `clear_test_data()` 后 `seed_test_data()`;
    - 这是 `POST /api/v1/_test/reset` 与本模块 CLI 入口的唯一实现路径。
    """
    clear_test_data()
    seed_test_data()
    print("[reset_test_data] done")


if __name__ == "__main__":
    """命令行入口。

    默认行为:
        - 若表不存在则建表,再补充缺失的 Seed 数据(`init_db()` + `seed_db()`)。
    兼容旧用法(已废弃):
        - 带 `--reset`:等价于 `reset_test_data()`(旧名 `seed_full`)。
        - 带 `--full`:同 `--reset`。
    """
    import sys
    if "--reset" in sys.argv or "--full" in sys.argv:
        # 兼容旧调用:依然先建表再清空+灌入,确保脚本可以独立运行
        init_db()
        reset_test_data()
    else:
        init_db()
        seed_db()
    print("Seed done.")
