"""api_tests 全局 fixture + 配置。

约束:
    * /_test/reset 失败必须直接 pytest fail，绝不 except: pass。
    * reset_test_data 由 app.test_data 委托，本模块只通过 HTTP 调用。
"""
import os
import time

import httpx
import pytest

BASE_URL = os.getenv("AUTOSHOP_BASE", "http://127.0.0.1:8000") + "/api/v1"


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


def _call_reset(base_url: str) -> None:
    """HTTP 调用 /_test/reset;失败立即抛出,绝不允许 except: pass。"""
    url = f"{base_url}/_test/reset"
    resp = httpx.post(url, timeout=30.0)
    if resp.status_code != 200:
        pytest.fail(
            f"/_test/reset failed: HTTP {resp.status_code}, body={resp.text!r}. "
            f"Check that app is started with AUTOSHOP_ENV=test and AUTOSHOP_ENABLE_TEST_API=true."
        )


@pytest.fixture(scope="session")
def client() -> httpx.Client:
    """同步 client,所有用例共用一个 session。"""
    c = httpx.Client(base_url=BASE_URL, timeout=10.0)
    # 启动时确保数据库处于已知 mock 状态
    _call_reset(BASE_URL)
    yield c
    c.close()


@pytest.fixture
def fresh_user(client: httpx.Client):
    """每个用例级 fixture:注册一个全新用户并返回 (authed_client, username)。"""
    ts = int(time.time() * 1000)
    username = f"u_{ts}"
    password = "Test@123456"
    email = f"{username}@example.com"
    phone = "13800138000"

    r = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
            "email": email,
            "phone": phone,
        },
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
