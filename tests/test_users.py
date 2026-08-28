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
    client, _ = fresh_user
    r = client.put("/users/me", json={"phone": "12345"})
    assert r.status_code == 400
    assert_biz_code(r.json(), 40001)


def test_me_without_auth(client):
    r = client.get("/users/me")
    assert r.status_code == 401
    assert_biz_code(r.json(), 40101)


def test_update_me_without_auth(client):
    r = client.put("/users/me", json={"nickname": "hacker"})
    assert r.status_code == 401
    assert_biz_code(r.json(), 40101)
