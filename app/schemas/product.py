"""商品 Schemas"""
from pydantic import BaseModel, Field


class ProductListItem(BaseModel):
    productId: int
    name: str
    category: str
    price: float
    stock: int
    status: str


class ProductDetail(BaseModel):
    productId: int
    name: str
    description: str | None
    category: str
    price: float
    stock: int
    status: str


class ProductListData(BaseModel):
    list: list[ProductListItem]
    page: int = Field(default=1, ge=1)
    pageSize: int = Field(default=10, ge=1, le=100)
    total: int
