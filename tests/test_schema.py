"""JSON Schema 校验"""
import re

import pytest

from .utils import assert_envelope


ORDER_DETAIL_SCHEMA = {
    "type": "object",
    "required": ["code", "message", "data", "timestamp", "requestId"],
    "properties": {
        "code": {"type": "integer"},
        "message": {"type": "string"},
        "timestamp": {"type": "integer", "minimum": 0},
        "requestId": {"type": "string", "pattern": r"^req_"},
        "data": {
            "type": "object",
            "required": ["orderId", "orderNo", "orderStatus", "paymentStatus",
                         "totalAmount", "items", "receiver", "createdAt"],
            "properties": {
                "orderId":       {"type": "integer", "minimum": 1},
                "orderNo":       {"type": "string", "pattern": r"^MOCK\d{12}\d{4}$"},
                "orderStatus":   {"enum": ["PAID", "PAY_FAILED", "PENDING_PAYMENT"]},
                "paymentStatus": {"enum": ["MOCK_SUCCESS", "MOCK_FAILED", "MOCK_PENDING"]},
                "totalAmount":   {"type": "number", "minimum": 0},
                "createdAt":     {"type": "string"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["productId", "productName", "quantity", "unitPrice", "amount"],
                    },
                },
            },
        },
    },
}


@pytest.fixture(autouse=True)
def reset_before_each(client):
    client.post("/_test/reset")


def test_order_detail_matches_json_schema(client, fresh_user):
    import jsonschema
    fclient, _ = fresh_user
    r = fclient.post("/cart/items", json={"productId": 1001, "quantity": 1})
    cart_item_id = r.json()["data"]["cartItemId"]

    r = fclient.post("/orders", json={
        "cartItemIds": [cart_item_id],
        "receiver": {"name": "x", "phone": "13800138000", "address": "y"},
        "mockResult": "SUCCESS",
    })
    order_id = r.json()["data"]["orderId"]

    r = fclient.get(f"/orders/{order_id}")
    jsonschema.validate(r.json(), ORDER_DETAIL_SCHEMA)
