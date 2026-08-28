"""认证接口测试"""
import pytest

from .utils import assert_biz_code, assert_envelope, gen_email, gen_username


def test_register_and_login(client):
    username = gen_username()
    password = "Test@123456"
    email = gen_email(username)
    phone = "13800138000"

    # 注册
    r = client.post("/auth/register", json={
        "username": username, "password": password,
        "email": email, "phone": phone,
    })
    assert r.status_code == 200
    data = assert_envelope(r.json())
    assert data["username"] == username
    assert isinstance(data["userId"], int) and data["userId"] > 0

    # 登录
    r = client.post("/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200
    data = assert_envelope(r.json())
    assert data["tokenType"] == "Bearer"
    assert data["expiresIn"] == 7200
    assert data["accessToken"].count(".") == 2  # JWT 三段


def test_register_duplicate_username(client):
    username = gen_username()
    payload = {"username": username, "password": "Test@123456", "email": gen_email(username)}
    r1 = client.post("/auth/register", json=payload)
    assert r1.json()["code"] == 200
    # 改 email 再用同一 username
    payload["email"] = gen_email(username + "_2")
    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == 409
    assert_biz_code(r2.json(), 40901)


def test_register_username_too_short(client):
    r = client.post("/auth/register", json={
        "username": "abc", "password": "Test@123456", "email": "abc@x.com",
    })
    assert r.status_code == 400
    assert_biz_code(r.json(), 40001)


def test_register_password_too_short(client):
    r = client.post("/auth/register", json={
        "username": gen_username(), "password": "short", "email": gen_email("x"),
    })
    assert r.status_code == 400
    assert_biz_code(r.json(), 40001)


def test_login_wrong_password(client):
    username = gen_username()
    client.post("/auth/register", json={
        "username": username, "password": "Test@123456", "email": gen_email(username),
    })
    r = client.post("/auth/login", json={"username": username, "password": "WrongPass1"})
    assert r.status_code == 401
    assert_biz_code(r.json(), 40101)


def test_login_user_not_exists(client):
    r = client.post("/auth/login", json={"username": "no_such_user", "password": "Test@123456"})
    assert r.status_code == 401
    assert_biz_code(r.json(), 40101)
