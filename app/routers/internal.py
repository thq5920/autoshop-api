"""测试用内部接口(仅当 DEBUG=true 时启用)。

`POST /api/v1/_test/reset` 现在统一委托给 `app.seed.reset_test_data()`,
后者是 `clear_test_data()` + `seed_test_data()` 的标准组合,
不再使用 DROP TABLE + CREATE TABLE 的硬重置逻辑。
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.response import ok
from app.seed import reset_test_data

router = APIRouter(prefix="/_test", tags=["test-only"])


@router.post("/reset", response_model=None)
def reset(db: Session = Depends(get_db)):
    """重置数据库:清空所有数据(TRUNCATE) + 重新插入固定 Seed 数据。

    仅供自动化测试使用,DEBUG=false 时禁用。
    业务数据 + 表结构 + Schema 的完整性由 Python 端 (`app.seed`) 统一维护,
    这里不直接 import 任何 Model,以保持接口层职责单一。
    """
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="disabled in production")

    # `db` 参数是为 FastAPI 依赖注入保留,实际重置逻辑在独立 Session 里执行
    del db
    reset_test_data()

    return ok(data={"resetAt": int(datetime.now(timezone.utc).timestamp() * 1000)})
