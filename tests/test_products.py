"""商品接口测试"""
import pytest

from .utils import assert_biz_code, assert_envelope


def test_list_products_default(client):
    r = client.get("/products")
    assert r.status_code == 200
    data = assert_envelope(r.json())
    assert "list" in data and "total" in data and "page" in data and "pageSize" in data
    assert data["page"] == 1 and data["pageSize"] == 10
    # 至少要有 4 个种子商品
    assert data["total"] >= 4


def test_list_products_filter_keyword(client):
    r = client.get("/products", params={"keyword": "iphone"})
    data = assert_envelope(r.json())
    assert data["total"] >= 1
    for p in data["list"]:
        assert "iphone" in p["name"].lower()


def test_list_products_filter_price_range(client):
    r = client.get("/products", params={"minPrice": 1000, "maxPrice": 7000})
    data = assert_envelope(r.json())
    for p in data["list"]:
        assert 1000 <= p["price"] <= 7000


def test_list_products_pagination(client):
    r = client.get("/products", params={"page": 1, "pageSize": 2})
    data = assert_envelope(r.json())
    assert data["pageSize"] == 2
    assert len(data["list"]) <= 2


def test_get_product_detail(client):
    r = client.get("/products/1001")
    data = assert_envelope(r.json())
    assert data["productId"] == 1001
    assert data["status"] == "ON_SALE"


def test_get_product_not_found(client):
    r = client.get("/products/99999")
    assert r.status_code == 404
    assert_biz_code(r.json(), 40501)  # PRODUCT_NOT_FOUND


def test_get_off_shelf_product(client):
    r = client.get("/products/1004")
    data = assert_envelope(r.json())
    assert data["status"] == "OFF_SHELF"


def test_get_out_of_stock_product(client):
    r = client.get("/products/1003")
    data = assert_envelope(r.json())
    assert data["stock"] == 0
    assert data["status"] == "ON_SALE"
