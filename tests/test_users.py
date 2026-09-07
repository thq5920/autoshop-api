"""个人中心接口测试"""
import pytest

from .utils import assert_biz_code, assert_envelope


@pytest.fixture(autouse=True)
def reset_before_each(client):
    client.post("/_test/reset")


def test_get_me(fresh_user):
    client, username = fresh_user
    r = client.get("/users/me")
    data = assert_envelope(r.json())
    assert data["username"] == username
    assert data["userId"] > 0
    assert data["email"].endswith("@example.com")
    assert "T" in data["createdAt"]


def test_update_me(fresh_user):
    client, _ = fresh_user
    r = client.put("/users/me", json={"nickname": "Auto Tester", "phone": "13900139000"})
    data = assert_envelope(r.json())
    assert data["nickname"] == "Auto Tester"
    assert data["phone"] == "13900139000"

    # 校验持久化
    r = client.get("/users/me")
    me = assert_envelope(r.json())
    assert me["nickname"] == "Auto Tester"
    assert me["phone"] == "13900139000"


def test_update_me_invalid_phone(fresh_user):
    """手机号格式错误 → 422 + 40209 PHONE_FORMAT_ERROR"""
    client, _ = fresh_user
    r = client.put("/users/me", json={"phone": "12345"})
    assert r.status_code == 422
    assert_biz_code(r.json(), 40209)


def test_update_me_nickname_too_long(fresh_user):
    """昵称过长 → 422 + 40210 NICKNAME_TOO_LONG"""
    client, _ = fresh_user
    r = client.put("/users/me", json={"nickname": "x" * 51})
    assert r.status_code == 422
    assert_biz_code(r.json(), 40210)


def test_update_me_no_fields(fresh_user):
    """没传任何字段 → 400 + 40402 NO_UPDATE_FIELDS"""
    client, _ = fresh_user
    r = client.put("/users/me", json={})
    assert r.status_code == 400
    assert_biz_code(r.json(), 40402)


def test_me_without_auth(client):
    r = client.get("/users/me")
    assert r.status_code == 401
    assert_biz_code(r.json(), 40101)


def test_update_me_without_auth(client):
    r = client.put("/users/me", json={"nickname": "hacker"})
    assert r.status_code == 401
    assert_biz_code(r.json(), 40101)
