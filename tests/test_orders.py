"""订单接口测试(包含 Mock 三态参数化)"""
import re

import pytest

from .utils import assert_biz_code, assert_envelope


RECEIVER = {
    "name": "张三",
    "phone": "13800138000",
    "address": "上海市浦东新区测试路100号",
}


@pytest.fixture(autouse=True)
def reset_before_each(client):
    client.post("/_test/reset")


def _prepare_cart(client, product_id=1001, quantity=2):
    r = client.post("/cart/items", json={"productId": product_id, "quantity": quantity})
    assert r.json()["code"] == 200
    return r.json()["data"]["cartItemId"]


@pytest.mark.parametrize("mock_result, expected_order_status, expected_payment_status", [
    ("SUCCESS", "PAID",            "MOCK_SUCCESS"),
    ("FAIL",    "PAY_FAILED",      "MOCK_FAILED"),
    ("PENDING", "PENDING_PAYMENT", "MOCK_PENDING"),
])
def test_create_order_with_mock_results(
    fresh_user, mock_result, expected_order_status, expected_payment_status
):
    client, _ = fresh_user
    cart_item_id = _prepare_cart(client)

    r = client.post("/orders", json={
        "cartItemIds": [cart_item_id],
        "receiver": RECEIVER,
        "remark": "接口自动化测试订单",
        "mockResult": mock_result,
    })
    data = assert_envelope(r.json())
    assert data["orderStatus"] == expected_order_status
    assert data["paymentStatus"] == expected_payment_status
    assert data["totalAmount"] == 11998.00
    assert re.match(r"^MOCK\d{12}\d{4}$", data["orderNo"])
    assert "T" in data["createdAt"]  # ISO8601


def test_create_order_default_mock_is_success(fresh_user):
    client, _ = fresh_user
    cart_item_id = _prepare_cart(client)
    r = client.post("/orders", json={
        "cartItemIds": [cart_item_id],
        "receiver": RECEIVER,
    })
    data = assert_envelope(r.json())
    assert data["orderStatus"] == "PAID"
    assert data["paymentStatus"] == "MOCK_SUCCESS"


def test_create_order_invalid_cart_item(fresh_user):
    client, _ = fresh_user
    r = client.post("/orders", json={
        "cartItemIds": [9999999],
        "receiver": RECEIVER,
    })
    assert r.status_code == 404
    assert_biz_code(r.json(), 40601)  # CART_ITEM_NOT_FOUND


def test_create_order_off_shelf_product(fresh_user):
    client, _ = fresh_user
    cart_item_id = _prepare_cart(client, product_id=1004)
    r = client.post("/orders", json={
        "cartItemIds": [cart_item_id],
        "receiver": RECEIVER,
    })
    assert r.status_code == 400
    assert_biz_code(r.json(), 40502)  # PRODUCT_OFF_SHELF


def test_create_order_insufficient_stock(fresh_user):
    client, _ = fresh_user
    # AirPods 库存 0 → 加车时就被 INSUFFICIENT_STOCK 拒绝
    r = client.post("/cart/items", json={"productId": 1003, "quantity": 1})
    assert r.status_code == 400
    assert_biz_code(r.json(), 40503)


def test_list_my_orders(fresh_user):
    client, _ = fresh_user
    cart_item_id = _prepare_cart(client)
    client.post("/orders", json={"cartItemIds": [cart_item_id], "receiver": RECEIVER})

    r = client.get("/orders")
    data = assert_envelope(r.json())
    assert data["total"] >= 1
    assert len(data["list"]) >= 1


def test_list_orders_filter_status(fresh_user):
    client, _ = fresh_user
    cart_item_id = _prepare_cart(client)
    client.post("/orders", json={
        "cartItemIds": [cart_item_id], "receiver": RECEIVER, "mockResult": "FAIL",
    })
    r = client.get("/orders", params={"status": "PAY_FAILED"})
    data = assert_envelope(r.json())
    assert data["total"] >= 1
    for o in data["list"]:
        assert o["orderStatus"] == "PAY_FAILED"


def test_get_order_detail(fresh_user):
    client, _ = fresh_user
    cart_item_id = _prepare_cart(client)
    r = client.post("/orders", json={"cartItemIds": [cart_item_id], "receiver": RECEIVER})
    order_id = r.json()["data"]["orderId"]

    r = client.get(f"/orders/{order_id}")
    detail = assert_envelope(r.json())
    assert detail["orderId"] == order_id
    assert detail["orderStatus"] == "PAID"
    assert len(detail["items"]) == 1
    assert detail["items"][0]["productId"] == 1001
    assert detail["receiver"]["name"] == "张三"


def test_get_order_detail_not_found(fresh_user):
    client, _ = fresh_user
    r = client.get("/orders/9999999")
    assert r.status_code == 404
    assert_biz_code(r.json(), 40701)  # ORDER_NOT_FOUND


def test_order_without_auth(client):
    r = client.post("/orders", json={"cartItemIds": [1], "receiver": RECEIVER})
    assert r.status_code == 401
    assert_biz_code(r.json(), 40101)  # UNAUTHORIZED
