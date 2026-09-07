"""购物车接口测试"""
import pytest

from .utils import assert_biz_code, assert_envelope


@pytest.fixture(autouse=True)
def reset_before_each(client):
    """每个用例开始前重置数据,保证用例相互独立"""
    client.post("/_test/reset")


def test_add_to_cart_and_list(fresh_user):
    client, _ = fresh_user
    # 加车
    r = client.post("/cart/items", json={"productId": 1001, "quantity": 2})
    data = assert_envelope(r.json())
    assert data["productId"] == 1001
    assert data["quantity"] == 2
    assert data["unitPrice"] == 5999.00
    assert data["totalAmount"] == 11998.00

    # 列表
    r = client.get("/cart")
    cart = assert_envelope(r.json())
    assert cart["totalQuantity"] == 2
    assert cart["totalAmount"] == 11998.00
    assert len(cart["items"]) == 1
    assert cart["items"][0]["productName"] == "iPhone 17"


def test_add_to_cart_out_of_stock(fresh_user):
    client, _ = fresh_user
    r = client.post("/cart/items", json={"productId": 1003, "quantity": 1})
    assert r.status_code == 400
    assert_biz_code(r.json(), 40503)  # INSUFFICIENT_STOCK


def test_add_to_cart_off_shelf(fresh_user):
    client, _ = fresh_user
    r = client.post("/cart/items", json={"productId": 1004, "quantity": 1})
    assert r.status_code == 400
    assert_biz_code(r.json(), 40502)  # PRODUCT_OFF_SHELF


def test_add_to_cart_product_not_found(fresh_user):
    client, _ = fresh_user
    r = client.post("/cart/items", json={"productId": 99999, "quantity": 1})
    assert r.status_code == 404
    assert_biz_code(r.json(), 40501)  # PRODUCT_NOT_FOUND


def test_update_cart_item_quantity(fresh_user):
    client, _ = fresh_user
    r = client.post("/cart/items", json={"productId": 1001, "quantity": 1})
    cart_item_id = r.json()["data"]["cartItemId"]

    r = client.put(f"/cart/items/{cart_item_id}", json={"quantity": 3})
    data = assert_envelope(r.json())
    assert data["quantity"] == 3
    assert data["totalAmount"] == 17997.00


def test_update_cart_item_not_found(fresh_user):
    client, _ = fresh_user
    r = client.put("/cart/items/9999999", json={"quantity": 1})
    assert r.status_code == 404
    assert_biz_code(r.json(), 40601)  # CART_ITEM_NOT_FOUND


def test_delete_cart_item(fresh_user):
    client, _ = fresh_user
    r = client.post("/cart/items", json={"productId": 1001, "quantity": 1})
    cart_item_id = r.json()["data"]["cartItemId"]

    r = client.delete(f"/cart/items/{cart_item_id}")
    assert_envelope(r.json())

    r = client.get("/cart")
    assert r.json()["data"]["items"] == []


def test_cart_without_auth(client):
    r = client.get("/cart")
    assert r.status_code == 401
    assert_biz_code(r.json(), 40101)  # UNAUTHORIZED


def test_add_to_cart_without_auth(client):
    r = client.post("/cart/items", json={"productId": 1001, "quantity": 1})
    assert r.status_code == 401
    assert_biz_code(r.json(), 40101)


def test_add_to_cart_quantity_invalid(fresh_user):
    """Pydantic Field(ge=1) 拦截 quantity=0 → 422 + 40001(数量约束通用码)"""
    client, _ = fresh_user
    r = client.post("/cart/items", json={"productId": 1001, "quantity": 0})
    assert r.status_code == 422
    # quantity 是 Pydantic Field 约束,落到 PARAM_INVALID 兜底
    assert_biz_code(r.json(), 40001)
