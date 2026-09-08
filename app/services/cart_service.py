"""购物车服务。

由于项目刻意不在数据库层引入 FOREIGN KEY、且 Model 上不声明 `relationship()`,
所有跨 Model 的属性访问都必须通过显式 `db.get(Model, id)` 取得,
避免 Lazy/Auto load 触发不存在的关联。
"""
from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions import BizCode, BizException
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartData, CartItemView


def add_to_cart(db: Session, user: User, product_id: int, quantity: int) -> CartItem:
    product = db.get(Product, product_id)
    if not product:
        raise BizException(BizCode.PRODUCT_NOT_FOUND, http_status=404)

    # 注意:已下架的商品仍允许加入购物车,以便"用户保存待上架后再下单";
    # 真正的 OFF_SHELF 拦截放在订单创建链路 (`order_service.create_order`)。
    # 这里仅校验库存上限。

    existing = (
        db.query(CartItem)
        .filter(CartItem.user_id == user.id, CartItem.product_id == product_id)
        .first()
    )

    new_qty = quantity if not existing else existing.quantity + quantity
    if new_qty > product.stock:
        raise BizException(BizCode.INSUFFICIENT_STOCK, http_status=400)

    if existing:
        existing.quantity = new_qty
        db.commit()
        db.refresh(existing)
        return existing

    item = CartItem(
        user_id=user.id,
        product_id=product_id,
        quantity=quantity,
        unit_price=float(product.price),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_cart(db: Session, user: User) -> CartData:
    """查询当前用户购物车。

    按 `CartItem.product_id` 逐条显式加载 Product,
    商品被删除/不存在时按 40501 商品不存在处理,而不是依赖不存在的 ORM 关联。
    """
    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    views: list[CartItemView] = []
    total_qty = 0
    total_amount = Decimal("0")

    for it in items:
        product = db.get(Product, it.product_id)
        if product is None:
            # 逻辑关联:商品记录缺失时按 PRODUCT_NOT_FOUND 抛出,
            # 不再静默走 `it.product.name` 这条不存在的 ORM 路径。
            raise BizException(BizCode.PRODUCT_NOT_FOUND, http_status=404)
        amount = Decimal(str(it.unit_price)) * it.quantity
        views.append(
            CartItemView(
                cartItemId=it.id,
                productId=it.product_id,
                productName=product.name,
                quantity=it.quantity,
                unitPrice=float(it.unit_price),
                totalAmount=float(amount),
            )
        )
        total_qty += it.quantity
        total_amount += amount

    return CartData(
        items=views,
        totalQuantity=total_qty,
        totalAmount=float(total_amount.quantize(Decimal("0.01"))),
    )


def update_cart_item(db: Session, user: User, cart_item_id: int, quantity: int) -> CartItem:
    item = db.get(CartItem, cart_item_id)
    if not item or item.user_id != user.id:
        raise BizException(BizCode.CART_ITEM_NOT_FOUND, http_status=404)

    # 显式加载关联商品以便校验库存,不再依赖 `item.product.stock`。
    product = db.get(Product, item.product_id)
    if product is None:
        raise BizException(BizCode.PRODUCT_NOT_FOUND, http_status=404)
    if quantity > product.stock:
        raise BizException(BizCode.INSUFFICIENT_STOCK, http_status=400)

    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item


def delete_cart_item(db: Session, user: User, cart_item_id: int) -> None:
    item = db.get(CartItem, cart_item_id)
    if not item or item.user_id != user.id:
        raise BizException(BizCode.CART_ITEM_NOT_FOUND, http_status=404)
    db.delete(item)
    db.commit()
