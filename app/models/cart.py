"""购物车模型"""
from sqlalchemy import Column, DateTime, Index, Integer, Numeric, String, UniqueConstraint

from app.database import Base


class CartItem(Base):
    """购物车明细表"""
    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product"),
        Index("ix_cart_user_id", "user_id"),
        {"mysql_comment": "购物车明细表"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="购物车项ID")
    user_id = Column(Integer, nullable=False, comment="用户ID，逻辑关联 users.id")
    product_id = Column(Integer, nullable=False, comment="商品ID，逻辑关联 products.id")
    quantity = Column(Integer, nullable=False, default=1, comment="商品数量")
    unit_price = Column(Numeric(10, 2), nullable=False, comment="加入购物车时商品单价快照")
    created_at = Column(DateTime, nullable=True, comment="加入购物车时间")
