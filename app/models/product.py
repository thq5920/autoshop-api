"""商品模型"""
from sqlalchemy import Column, Integer, Numeric, String

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True, default="AutoShop Test Product")
    category = Column(String(50), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    status = Column(String(20), nullable=False, default="ON_SALE")  # ON_SALE / OFF_SHELF
