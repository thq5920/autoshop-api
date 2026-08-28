"""FastAPI 入口"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.exceptions import register_exception_handlers
from app.response import ok
from app.routers import auth, cart, internal, orders, products, users
from app.seed import seed_if_empty


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="专门用于接口自动化测试练习的 Mock 商城 API",
    )

    register_exception_handlers(app)

    @app.get("/healthz", include_in_schema=False)
    def healthz():
        return JSONResponse(content=ok(data={"status": "ok"}).model_dump(by_alias=True))

    api_prefix = settings.API_PREFIX
    app.include_router(auth.router, prefix=api_prefix)
    app.include_router(products.router, prefix=api_prefix)
    app.include_router(cart.router, prefix=api_prefix)
    app.include_router(orders.router, prefix=api_prefix)
    app.include_router(users.router, prefix=api_prefix)
    app.include_router(internal.router, prefix=api_prefix)

    @app.on_event("startup")
    def _startup():
        init_db()
        seed_if_empty()

    return app


app = create_app()
