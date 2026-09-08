"""订单服务。

由于项目刻意不在数据库层引入 FOREIGN KEY、且 Model 上不声明 `relationship()`,
所有跨 Model 的属性访问都必须通过显式 `db.get(Model, id)` /
`db.query(Model).filter(...).all()` 取得,避免 Lazy/Auto load 触发不存在的关联。
"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions import BizCode, BizException
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import CreateOrderData, CreateOrderRequest, OrderDetail, OrderItemView


_MOCK_STATUS_MAP = {
    "SUCCESS": ("PAID", "MOCK_SUCCESS"),
    "FAIL": ("PAY_FAILED", "MOCK_FAILED"),
    "PENDING": ("PENDING_PAYMENT", "MOCK_PENDING"),
}


def _gen_order_no(user_id: int) -> str:
    # %Y%m%d%H%M%S = 14 位;但测试与 JSON Schema 都按 12 位 %y%m%d%H%M%S 来断言,
    # 这里统一改为 12 位短格式以保持一致。
    return f"MOCK{datetime.now().strftime('%y%m%d%H%M%S')}{user_id:04d}"


def _load_products_map(db: Session, product_ids: set[int]) -> dict[int, Product]:
    """一次性按 ID 列表预加载 Product,避免在循环里 N+1。"""
    if not product_ids:
        return {}
    rows = db.query(Product).filter(Product.id.in_(product_ids)).all()
    return {p.id: p for p in rows}


def create_order(
    db: Session, user: User, req: CreateOrderRequest
) -> CreateOrderData:
    if not req.cartItemIds:
        raise BizException(BizCode.CART_EMPTY, http_status=400)

    items = (
        db.query(CartItem)
        .filter(CartItem.user_id == user.id, CartItem.id.in_(req.cartItemIds))
        .all()
    )
    if len(items) != len(set(req.cartItemIds)):
        raise BizException(BizCode.CART_ITEM_NOT_FOUND, http_status=404)

    # 显式预加载所有涉及商品,后续业务校验 / 扣库存都用查到的 Product,
    # 不再依赖 `it.product.status` / `it.product.stock` / `it.product.name`。
    products = _load_products_map(db, {it.product_id for it in items})

    for it in items:
        product = products.get(it.product_id)
        if product is None:
            raise BizException(BizCode.PRODUCT_NOT_FOUND, http_status=404)
        if product.status != "ON_SALE":
            raise BizException(BizCode.PRODUCT_OFF_SHELF, http_status=400)
        if it.quantity > product.stock:
            raise BizException(BizCode.INSUFFICIENT_STOCK, http_status=400)

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
    db.flush()

    for it in items:
        product = products[it.product_id]
        line_amount = Decimal(str(it.unit_price)) * it.quantity
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=it.product_id,
                product_name=product.name,
                quantity=it.quantity,
                unit_price=float(it.unit_price),
                amount=float(line_amount.quantize(Decimal("0.01"))),
            )
        )
        # 通过 ORM 实例修改库存,SQLAlchemy 会在 flush 时正确生成 UPDATE。
        product.stock -= it.quantity
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
        raise BizException(BizCode.ORDER_NOT_FOUND, http_status=404)

    # 显式查询 OrderItem,不再访问不存在的 `order.items`。
    items = (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order.id)
        .all()
    )
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
            for oi in items
        ],
        receiver=order.receiver,
        createdAt=order.created_at,
    )
