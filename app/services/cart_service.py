"""购物车服务"""
from sqlalchemy.orm import Session

from app.exceptions import BizCode, BizException
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartData, CartItemView


def add_to_cart(db: Session, user: User, product_id: int, quantity: int) -> CartItem:
    product = db.get(Product, product_id)
    if not product:
        raise BizException(BizCode.NOT_FOUND, "Product not found", 404)
    if product.status != "ON_SALE":
        raise BizException(BizCode.PRODUCT_OFF_SHELF, "Product is off shelf", 400)

    existing = (
        db.query(CartItem)
        .filter(CartItem.user_id == user.id, CartItem.product_id == product_id)
        .first()
    )

    new_qty = quantity if not existing else existing.quantity + quantity
    if new_qty > product.stock:
        raise BizException(BizCode.PARAM_INVALID, "Insufficient stock", 400)

    if existing:
        existing.quantity = new_qty
        db.commit()
        db.refresh(existing)
        return existing

    item = CartItem(
        user_id=user.id,
        product_id=product_id,
        quantity=quantity,
        unit_price=product.price,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_cart(db: Session, user: User) -> CartData:
    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    views: list[CartItemView] = []
    total_qty = 0
    total_amount = 0.0
    for it in items:
        amount = it.unit_price * it.quantity
        views.append(
            CartItemView(
                cartItemId=it.id,
                productId=it.product_id,
                productName=it.product.name,
                quantity=it.quantity,
                unitPrice=it.unit_price,
                totalAmount=amount,
            )
        )
        total_qty += it.quantity
        total_amount += amount
    return CartData(items=views, totalQuantity=total_qty, totalAmount=round(total_amount, 2))


def update_cart_item(db: Session, user: User, cart_item_id: int, quantity: int) -> CartItem:
    item = db.get(CartItem, cart_item_id)
    if not item or item.user_id != user.id:
        raise BizException(BizCode.NOT_FOUND, "Cart item not found", 404)
    if quantity > item.product.stock:
        raise BizException(BizCode.PARAM_INVALID, "Insufficient stock", 400)
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item


def delete_cart_item(db: Session, user: User, cart_item_id: int) -> None:
    item = db.get(CartItem, cart_item_id)
    if not item or item.user_id != user.id:
        raise BizException(BizCode.NOT_FOUND, "Cart item not found", 404)
    db.delete(item)
    db.commit()
