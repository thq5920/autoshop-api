"""购物车 Schemas"""
from pydantic import BaseModel, Field


class AddCartItemRequest(BaseModel):
    productId: int
    quantity: int = Field(ge=1, le=9999)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(ge=1, le=9999)


class AddCartItemData(BaseModel):
    cartItemId: int
    productId: int
    quantity: int
    unitPrice: float
    totalAmount: float


class UpdateCartItemData(BaseModel):
    cartItemId: int
    quantity: int
    totalAmount: float


class CartItemView(BaseModel):
    cartItemId: int
    productId: int
    productName: str
    quantity: int
    unitPrice: float
    totalAmount: float


class CartData(BaseModel):
    items: list[CartItemView]
    totalQuantity: int
    totalAmount: float
