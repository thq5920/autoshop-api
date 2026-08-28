"""业务链路一条龙:注册→登录→商品→加车→下单→订单→个人中心"""
import re

import pytest

from .utils import assert_envelope, gen_username


@pytest.fixture(autouse=True)
def reset_before_each(client):
    client.post("/_test/reset")


def test_full_business_flow(client):
    """文档 §19 推荐链路"""
    # 1. 生成随机用户名 + 注册
    username = gen_username()
    password = "Test@123456"
    r = client.post("/auth/register", json={
        "username": username, "password": password,
        "email": f"{username}@example.com", "phone": "13800138000",
    })
    user_id = assert_envelope(r.json())["userId"]

    # 2. 登录 + 提取 accessToken
    r = client.post("/auth/login", json={"username": username, "password": password})
    token = assert_envelope(r.json())["accessToken"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. 查询商品 + 提取 productId
    r = client.get("/products")
    products = assert_envelope(r.json())["list"]
    product_id = next(p["productId"] for p in products if p["status"] == "ON_SALE" and p["stock"] > 0)
    unit_price = next(p["price"] for p in products if p["productId"] == product_id)

    # 4. 加入购物车
    r = client.post("/cart/items", json={"productId": product_id, "quantity": 2}, headers=headers)
    cart_item_id = assert_envelope(r.json())["cartItemId"]
    expected_amount = unit_price * 2

    # 5. 查询购物车 + 断言金额
    r = client.get("/cart", headers=headers)
    cart = assert_envelope(r.json())
    assert cart["totalQuantity"] == 2
    assert cart["totalAmount"] == expected_amount

    # 6. Mock 下单
    r = client.post("/orders", json={
        "cartItemIds": [cart_item_id],
        "receiver": {
            "name": "张三", "phone": "13800138000",
            "address": "上海市浦东新区测试路100号",
        },
        "remark": "链路测试订单",
        "mockResult": "SUCCESS",
    }, headers=headers)
    order = assert_envelope(r.json())
    order_id = order["orderId"]
    order_no = order["orderNo"]

    assert re.match(r"^MOCK\d{12}\d{4}$", order_no)
    assert order["orderStatus"] == "PAID"
    assert order["paymentStatus"] == "MOCK_SUCCESS"
    assert order["totalAmount"] == expected_amount

    # 7. 查询订单详情
    r = client.get(f"/orders/{order_id}", headers=headers)
    detail = assert_envelope(r.json())
    assert detail["orderId"] == order_id
    assert detail["orderNo"] == order_no
    assert detail["orderStatus"] == "PAID"
    assert len(detail["items"]) == 1
    assert detail["items"][0]["productId"] == product_id

    # 8. 查询个人中心
    r = client.get("/users/me", headers=headers)
    me = assert_envelope(r.json())
    assert me["userId"] == user_id
    assert me["username"] == username
