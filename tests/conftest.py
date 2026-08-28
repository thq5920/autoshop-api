"""pytest 全局 fixture + 配置"""
import os
import time

import httpx
import pytest

BASE_URL = os.getenv("AUTOSHOP_BASE", "http://127.0.0.1:8000") + "/api/v1"


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def client() -> httpx.Client:
    """同步 client,所有用例共用一个 session"""
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as c:
        # 启动前重置一次(需要服务处于 DEBUG=true)
        try:
            c.post("/_test/reset")
        except Exception:
            pass
        yield c


@pytest.fixture
def fresh_user(client: httpx.Client):
    """每个用例级 fixture:注册一个全新用户并返回 (client_with_token, username, password)"""
    ts = int(time.time() * 1000)
    username = f"u_{ts}"
    password = "Test@123456"
    email = f"{username}@example.com"
    phone = "13800138000"

    r = client.post(
        "/auth/register",
        json={"username": username, "password": password, "email": email, "phone": phone},
    )
    assert r.status_code == 200, r.text
    assert r.json()["code"] == 200

    r = client.post("/auth/login", json={"username": username, "password": password})
    assert r.json()["code"] == 200
    token = r.json()["data"]["accessToken"]

    authed = httpx.Client(
        base_url=BASE_URL,
        timeout=10.0,
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        yield authed, username
    finally:
        authed.close()
