"""应用配置"""
import os
from urllib.parse import quote_plus

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings:
    APP_NAME: str = "AutoShop API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    # 数据库 —— MySQL
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "autoshop")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "autoshop")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "autoshop")
    MYSQL_CHARSET: str = os.getenv("MYSQL_CHARSET", "utf8mb4")

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        pw = quote_plus(self.MYSQL_PASSWORD)
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{pw}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
            f"?charset={self.MYSQL_CHARSET}"
        )

    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "autoshop-dev-secret-key-please-change-in-production-environment",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # bcrypt rounds
    BCRYPT_ROUNDS: int = int(os.getenv("BCRYPT_ROUNDS", "4"))

    # 环境
    @property
    def ENV(self) -> str:
        return os.getenv("AUTOSHOP_ENV", "dev")

    DEBUG: bool = os.getenv("AUTOSHOP_DEBUG", "true").lower() == "true"

    # 测试接口守门：ENV=test 且 ENABLE_TEST_API=true 才挂载 /_test/* 路由
    @property
    def ENABLE_TEST_API(self) -> bool:
        return (
            self.ENV.lower() == "test"
            and os.getenv("AUTOSHOP_ENABLE_TEST_API", "false").lower() == "true"
        )

    EXPOSE_AUTH_DETAIL: bool = os.getenv(
        "AUTOSHOP_EXPOSE_AUTH_DETAIL", "true"
    ).lower() == "true"


settings = Settings()
