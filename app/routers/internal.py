"""测试用内部接口。

只有当 app.config.settings.ENABLE_TEST_API == True 时才注册路由。
两个条件（AUTOSHOP_ENV=test 且 AUTOSHOP_ENABLE_TEST_API=true）都满足才挂载。
生产环境（任意一个不满足）此 Router 不会被挂载，请求 404。
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.response import ok
from app.test_data import reset_test_data

router = APIRouter(prefix="/_test", tags=["test-only"])

if not settings.ENABLE_TEST_API:
    # 生产环境：不挂载任何路由，请求返回 404
    router = None
else:

    @router.post("/reset", response_model=None)
    def reset(db: Session = Depends(get_db)):
        """重置数据库：清空所有数据（TRUNCATE）+ 重新插入固定 mock 数据。

        仅供自动化测试使用，必须 ENABLE_TEST_API == True。
        """
        del db  # 保留依赖注入保留字，实际重置在独立 Session 执行
        reset_test_data()
        return ok(data={"resetAt": int(datetime.now(timezone.utc).timestamp() * 1000)})
