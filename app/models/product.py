"""商品模型"""
from sqlalchemy import Column, Integer, Numeric, String

from app.database import Base


class Product(Base):
    """商品表"""
    __tablename__ = "products"
    __table_args__ = {"mysql_comment": "商品表"}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="商品ID")
    name = Column(String(100), nullable=False, comment="商品名称")
    description = Column(String(500), nullable=True, default="AutoShop Test Product", comment="商品描述")
    category = Column(String(50), nullable=False, index=True, comment="商品分类")
    price = Column(Numeric(10, 2), nullable=False, comment="商品单价")
    stock = Column(Integer, nullable=False, default=0, comment="当前库存数量")
    status = Column(
        String(20),
        nullable=False,
        default="ON_SALE",
        comment="商品状态（ON_SALE 在售 / OFF_SHELF 下架）",
    )
