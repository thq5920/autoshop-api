"""应用配置"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    APP_NAME: str = "AutoShop API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    # 数据库
    DB_PATH: str = os.getenv("AUTOSHOP_DB_PATH", str(BASE_DIR / "autoshop.db"))
    SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{DB_PATH}"

    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "autoshop-dev-secret-key-please-change-in-production-environment",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120  # 文档示例 expiresIn: 7200 秒 = 2h

    # bcrypt rounds (越低越快,测试场景可调到 4)
    BCRYPT_ROUNDS: int = int(os.getenv("BCRYPT_ROUNDS", "4"))

    # 环境
    ENV: str = os.getenv("AUTOSHOP_ENV", "dev")
    DEBUG: bool = os.getenv("AUTOSHOP_DEBUG", "true").lower() == "true"


settings = Settings()
