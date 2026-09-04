"""订单服务"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions import BizCode, BizException
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.user import User
from app.schemas.order import CreateOrderData, CreateOrderRequest, OrderDetail, OrderItemView


_MOCK_STATUS_MAP = {
    "SUCCESS": ("PAID", "MOCK_SUCCESS"),
    "FAIL": ("PAY_FAILED", "MOCK_FAILED"),
    "PENDING": ("PENDING_PAYMENT", "MOCK_PENDING"),
}


def _gen_order_no(user_id: int) -> str:
    return f"MOCK{datetime.now().strftime('%Y%m%d%H%M%S')}{user_id:04d}"


def create_order(
    db: Session, user: User, req: CreateOrderRequest
) -> CreateOrderData:
    items = (
        db.query(CartItem)
        .filter(CartItem.user_id == user.id, CartItem.id.in_(req.cartItemIds))
        .all()
    )
    if len(items) != len(set(req.cartItemIds)):
        raise BizException(BizCode.NOT_FOUND, "Cart item not found", 404)

    for it in items:
        if it.product.status != "ON_SALE":
            raise BizException(BizCode.PRODUCT_OFF_SHELF, "Product is off shelf", 400)
        if it.quantity > it.product.stock:
            raise BizException(BizCode.PARAM_INVALID, "Insufficient stock", 400)

    # Decimal 精确计算,避免浮点舍入误差
    total_amount = sum(
        Decimal(str(it.unit_price)) * it.quantity for it in items
    )
    total_amount = float(total_amount.quantize(Decimal("0.01")))

    mock_result = req.mockResult or "SUCCESS"
    order_status, payment_status = _MOCK_STATUS_MAP[mock_result]

    order = Order(
        order_no=_gen_order_no(user.id),
        user_id=user.id,
        total_amount=total_amount,
        order_status=order_status,
        payment_status=payment_status,
        receiver=req.receiver.model_dump(),
        remark=req.remark,
    )
    db.add(order)
    db.flush()  # 取 order.id

    for it in items:
        line_amount = Decimal(str(it.unit_price)) * it.quantity
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=it.product_id,
                product_name=it.product.name,
                quantity=it.quantity,
                unit_price=float(it.unit_price),
                amount=float(line_amount.quantize(Decimal("0.01"))),
            )
        )
        # 扣库存 + 删购物车
        it.product.stock -= it.quantity
        db.delete(it)

    db.commit()
    db.refresh(order)

    return CreateOrderData(
        orderId=order.id,
        orderNo=order.order_no,
        orderStatus=order.order_status,
        paymentStatus=order.payment_status,
        totalAmount=float(order.total_amount),
        createdAt=order.created_at,
    )


def list_orders(
    db: Session, user: User, page: int, page_size: int, status: str | None, order_no: str | None
) -> dict:
    q = db.query(Order).filter(Order.user_id == user.id)
    if status:
        q = q.filter(Order.order_status == status)
    if order_no:
        q = q.filter(Order.order_no == order_no)
    total = q.count()
    rows = (
        q.order_by(Order.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {
        "list": [
            {
                "orderId": o.id,
                "orderNo": o.order_no,
                "orderStatus": o.order_status,
                "totalAmount": float(o.total_amount),
                "createdAt": o.created_at,
            }
            for o in rows
        ],
        "page": page,
        "pageSize": page_size,
        "total": total,
    }


def get_order_detail(db: Session, user: User, order_id: int) -> OrderDetail:
    order = db.get(Order, order_id)
    if not order or order.user_id != user.id:
        raise BizException(BizCode.NOT_FOUND, "Order not found", 404)
    return OrderDetail(
        orderId=order.id,
        orderNo=order.order_no,
        orderStatus=order.order_status,
        paymentStatus=order.payment_status,
        totalAmount=float(order.total_amount),
        items=[
            OrderItemView(
                productId=oi.product_id,
                productName=oi.product_name,
                quantity=oi.quantity,
                unitPrice=float(oi.unit_price),
                amount=float(oi.amount),
            )
            for oi in order.items
        ],
        receiver=order.receiver,
        createdAt=order.created_at,
    )
