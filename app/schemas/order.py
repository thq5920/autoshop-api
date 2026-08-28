"""订单 Schemas"""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


MockResult = Literal["SUCCESS", "FAIL", "PENDING"]


class Receiver(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    phone: str = Field(pattern=r"^1[3-9]\d{9}$")
    address: str = Field(min_length=1, max_length=200)


class CreateOrderRequest(BaseModel):
    cartItemIds: list[int] = Field(min_length=1)
    receiver: Receiver
    remark: str | None = Field(default=None, max_length=200)
    mockResult: MockResult | None = "SUCCESS"  # 文档第 12 节

    @model_validator(mode="after")
    def _check_ids(self):
        if any(i <= 0 for i in self.cartItemIds):
            raise ValueError("cartItemIds must be positive integers")
        return self


class CreateOrderData(BaseModel):
    orderId: int
    orderNo: str
    orderStatus: str
    paymentStatus: str
    totalAmount: float
    createdAt: datetime


class OrderListItem(BaseModel):
    orderId: int
    orderNo: str
    orderStatus: str
    totalAmount: float
    createdAt: datetime


class OrderListData(BaseModel):
    list: list[OrderListItem]
    page: int
    pageSize: int
    total: int


class OrderItemView(BaseModel):
    productId: int
    productName: str
    quantity: int
    unitPrice: float
    amount: float


class OrderDetail(BaseModel):
    orderId: int
    orderNo: str
    orderStatus: str
    paymentStatus: str
    totalAmount: float
    items: list[OrderItemView]
    receiver: Receiver
    createdAt: datetime
