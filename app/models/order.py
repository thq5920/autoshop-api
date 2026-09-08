"""订单模型"""
from sqlalchemy import Column, DateTime, Index, Integer, JSON, Numeric, String

from app.database import Base


class Order(Base):
    """订单主表"""
    __tablename__ = "orders"
    __table_args__ = (
        Index("ix_orders_user_id", "user_id"),
        {"mysql_comment": "订单主表"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="订单ID")
    order_no = Column(
        String(32),
        unique=True,
        nullable=False,
        index=True,
        comment="订单编号",
    )
    user_id = Column(Integer, nullable=False, comment="用户ID，逻辑关联 users.id")
    total_amount = Column(Numeric(10, 2), nullable=False, comment="订单总金额")
    order_status = Column(
        String(32),
        nullable=False,
        comment="订单状态（PAID 已支付 / PAY_FAILED 支付失败 / PENDING_PAYMENT 待支付）",
    )
    payment_status = Column(
        String(32),
        nullable=False,
        comment="Mock支付状态（MOCK_SUCCESS / MOCK_FAILED / MOCK_PENDING）",
    )
    receiver = Column(JSON, nullable=False, comment="收货人信息JSON")
    remark = Column(String(200), nullable=True, comment="订单备注")
    created_at = Column(DateTime, nullable=False, comment="下单时间")


class OrderItem(Base):
    """订单商品明细表"""
    __tablename__ = "order_items"
    __table_args__ = (
        Index("ix_order_items_order_id", "order_id"),
        {"mysql_comment": "订单商品明细表"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="订单项ID")
    order_id = Column(Integer, nullable=False, comment="订单ID，逻辑关联 orders.id")
    product_id = Column(Integer, nullable=False, comment="商品ID，逻辑关联 products.id")
    product_name = Column(String(100), nullable=False, comment="下单时商品名称快照")
    quantity = Column(Integer, nullable=False, comment="购买数量")
    unit_price = Column(Numeric(10, 2), nullable=False, comment="下单时商品单价快照")
    amount = Column(Numeric(10, 2), nullable=False, comment="商品小计")
