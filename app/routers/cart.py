"""购物车路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.response import ok
from app.schemas.cart import (
    AddCartItemData,
    AddCartItemRequest,
    UpdateCartItemData,
    UpdateCartItemRequest,
)
from app.services.cart_service import (
    add_to_cart,
    delete_cart_item,
    list_cart,
    update_cart_item,
)

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=None)
def get_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ok(data=list_cart(db, user).model_dump())


@router.post("/items", response_model=None)
def add_item(
    req: AddCartItemRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = add_to_cart(db, user, req.productId, req.quantity)
    total = round(item.unit_price * item.quantity, 2)
    return ok(
        data=AddCartItemData(
            cartItemId=item.id,
            productId=item.product_id,
            quantity=item.quantity,
            unitPrice=item.unit_price,
            totalAmount=total,
        ).model_dump()
    )


@router.put("/items/{cart_item_id}", response_model=None)
def update_item(
    cart_item_id: int,
    req: UpdateCartItemRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = update_cart_item(db, user, cart_item_id, req.quantity)
    total = round(item.unit_price * item.quantity, 2)
    return ok(
        data=UpdateCartItemData(
            cartItemId=item.id,
            quantity=item.quantity,
            totalAmount=total,
        ).model_dump()
    )


@router.delete("/items/{cart_item_id}", response_model=None)
def delete_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    delete_cart_item(db, user, cart_item_id)
    return ok(data=None)
