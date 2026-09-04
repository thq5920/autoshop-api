"""商品路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import BizCode, BizException
from app.models.product import Product
from app.response import ok
from app.schemas.product import ProductListData, ProductListItem

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=None)
def list_products(
    page: int = 1,
    pageSize: int = 10,
    keyword: str | None = None,
    category: str | None = None,
    minPrice: float | None = None,
    maxPrice: float | None = None,
    db: Session = Depends(get_db),
):
    if page < 1:
        raise BizException(BizCode.PARAM_INVALID, "page must be >= 1", 400)
    if not (1 <= pageSize <= 100):
        raise BizException(BizCode.PARAM_INVALID, "pageSize must be in [1,100]", 400)

    q = db.query(Product)
    if keyword:
        q = q.filter(Product.name.like(f"%{keyword}%"))
    if category:
        q = q.filter(Product.category == category)
    if minPrice is not None:
        q = q.filter(Product.price >= minPrice)
    if maxPrice is not None:
        q = q.filter(Product.price <= maxPrice)

    total = q.count()
    rows = q.order_by(Product.id.asc()).offset((page - 1) * pageSize).limit(pageSize).all()

    return ok(
        data=ProductListData(
            list=[
                ProductListItem(
                    productId=p.id,
                    name=p.name,
                    category=p.category,
                    price=float(p.price),
                    stock=p.stock,
                    status=p.status,
                )
                for p in rows
            ],
            page=page,
            pageSize=pageSize,
            total=total,
        ).model_dump(mode="json"),
    )


@router.get("/{product_id}", response_model=None)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        raise BizException(BizCode.NOT_FOUND, "Product not found", 404)
    return ok(
        data={
            "productId": p.id,
            "name": p.name,
            "description": p.description,
            "category": p.category,
            "price": float(p.price),
            "stock": p.stock,
            "status": p.status,
        }
    )
