"""订单路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.response import ok
from app.schemas.order import (
    CreateOrderData,
    CreateOrderRequest,
    OrderDetail,
    OrderListData,
    OrderListItem,
)
from app.services.order_service import create_order, get_order_detail, list_orders

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=None)
def create(
    req: CreateOrderRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    data: CreateOrderData = create_order(db, user, req)
    return ok(data=data.model_dump(mode="json"))


@router.get("", response_model=None)
def list_my_orders(
    page: int = 1,
    pageSize: int = 10,
    status: str | None = None,
    orderNo: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    res = list_orders(db, user, page, pageSize, status, orderNo)
    return ok(
        data=OrderListData(
            list=[OrderListItem(**x) for x in res["list"]],
            page=res["page"],
            pageSize=res["pageSize"],
            total=res["total"],
        ).model_dump(mode="json")
    )


@router.get("/{order_id}", response_model=None)
def detail(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    detail_obj: OrderDetail = get_order_detail(db, user, order_id)
    return ok(data=detail_obj.model_dump(mode="json"))
