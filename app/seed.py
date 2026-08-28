"""种子数据:商品 + demo 用户"""
from app.database import SessionLocal
from app.models.product import Product
from app.models.user import User
from app.security import hash_password


PRODUCTS = [
    dict(id=1001, name="iPhone 17",            category="phone",    price=5999.00, stock=100, status="ON_SALE"),
    dict(id=1002, name="MacBook Air",          category="computer", price=7999.00, stock=50,  status="ON_SALE"),
    dict(id=1003, name="AirPods",              category="audio",    price=999.00,  stock=0,   status="ON_SALE"),
    dict(id=1004, name="Test Offline Product", category="test",     price=100.00,  stock=10,  status="OFF_SHELF"),
]


def seed_if_empty():
    """启动时调用:商品不存在则写入"""
    db = SessionLocal()
    try:
        if not db.query(Product).first():
            for p in PRODUCTS:
                db.add(Product(**p, description="AutoShop Test Product"))
            print("[seed] inserted", len(PRODUCTS), "products")
        # demo 用户(便于本地调试,不影响自动化)
        if not db.query(User).filter(User.username == "demo").first():
            db.add(User(
                username="demo",
                password_hash=hash_password("Demo@123456"),
                email="demo@example.com",
                phone="13800138000",
                nickname="演示用户",
            ))
            print("[seed] inserted demo user")
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    from app.database import init_db
    init_db()
    seed_if_empty()
    print("Seed done.")
