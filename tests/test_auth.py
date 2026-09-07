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
    assert_biz_code(r2.json(), 40901)  # USERNAME_ALREADY_EXISTS


def test_register_username_too_short(client):
    r = client.post("/auth/register", json={
        "username": "abc", "password": "Test@123456", "email": "abc@x.com",
    })
    assert r.status_code == 422
    assert_biz_code(r.json(), 40202)  # USERNAME_TOO_SHORT


def test_register_username_too_long(client):
    r = client.post("/auth/register", json={
        "username": "a" * 21, "password": "Test@123456", "email": "longname@x.com",
    })
    assert r.status_code == 422
    assert_biz_code(r.json(), 40203)  # USERNAME_TOO_LONG


def test_register_password_too_short(client):
    r = client.post("/auth/register", json={
        "username": gen_username(), "password": "short", "email": gen_email("x"),
    })
    assert r.status_code == 422
    assert_biz_code(r.json(), 40205)  # PASSWORD_TOO_SHORT


def test_register_password_too_long(client):
    r = client.post("/auth/register", json={
        "username": gen_username(), "password": "a" * 21, "email": gen_email("y"),
    })
    assert r.status_code == 422
    assert_biz_code(r.json(), 40206)  # PASSWORD_TOO_LONG


def test_register_email_format_error(client):
    r = client.post("/auth/register", json={
        "username": gen_username(), "password": "Test@123456", "email": "not-an-email",
    })
    assert r.status_code == 422
    assert_biz_code(r.json(), 40207)  # EMAIL_FORMAT_ERROR


def test_login_wrong_password(client):
    """DEBUG 模式下密码错误 → 40302 PASSWORD_INCORRECT"""
    username = gen_username()
    client.post("/auth/register", json={
        "username": username, "password": "Test@123456", "email": gen_email(username),
    })
    r = client.post("/auth/login", json={"username": username, "password": "WrongPass1"})
    assert r.status_code == 401
    assert_biz_code(r.json(), 40302)


def test_login_user_not_exists(client):
    """DEBUG 模式下账号不存在 → 40301 ACCOUNT_NOT_EXISTS"""
    r = client.post("/auth/login", json={"username": "no_such_user", "password": "Test@123456"})
    assert r.status_code == 401
    assert_biz_code(r.json(), 40301)


def test_login_wrong_password_en_locale(client):
    """Accept-Language: en-US 走英文 message,code 仍为 40302"""
    username = gen_username()
    client.post("/auth/register", json={
        "username": username, "password": "Test@123456", "email": gen_email(username),
    })
    r = client.post(
        "/auth/login",
        json={"username": username, "password": "WrongPass1"},
        headers={"Accept-Language": "en-US"},
    )
    assert r.status_code == 401
    assert_biz_code(r.json(), 40302)
    assert "password" in r.json()["message"].lower()
