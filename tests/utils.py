"""共用工具函数"""
from typing import Any


def assert_envelope(resp_json: dict, expected_code: int = 200) -> dict:
    """断言标准响应信封,返回 data

    message 默认是 i18n 表里的 "成功" / "success",不强制断言文案,
    如需校验文案请自行 assert resp_json["message"] == ...
    """
    assert "code" in resp_json, f"missing code: {resp_json}"
    assert "message" in resp_json
    assert "data" in resp_json
    assert "timestamp" in resp_json
    assert "requestId" in resp_json
    assert isinstance(resp_json["code"], int)
    assert resp_json["code"] == expected_code, (
        f"expected code={expected_code}, got {resp_json['code']}, msg={resp_json['message']}"
    )
    return resp_json["data"]


def assert_biz_code(resp_json: dict, expected_code: int) -> None:
    assert resp_json.get("code") == expected_code, (
        f"expected biz_code={expected_code}, got {resp_json.get('code')}, msg={resp_json.get('message')}"
    )


def gen_username() -> str:
    import time
    return f"u_{int(time.time()*1000)}"


def gen_email(u: str) -> str:
    return f"{u}@example.com"
