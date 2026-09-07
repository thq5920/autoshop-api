"""个人中心路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.exceptions import BizCode, BizException
from app.models.user import User
from app.response import ok
from app.schemas.user import MeData, UpdateMeData, UpdateMeRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=None)
def me(user: User = Depends(get_current_user)):
    return ok(
        data=MeData(
            userId=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            nickname=user.nickname,
            createdAt=user.created_at,
        ).model_dump(mode="json")
    )


@router.put("/me", response_model=None)
def update_me(
    req: UpdateMeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # 全部未传 → 40402 资料无任何更新
    if req.nickname is None and req.phone is None and req.email is None:
        raise BizException(BizCode.NO_UPDATE_FIELDS, http_status=400)

    if req.nickname is not None:
        user.nickname = req.nickname
    if req.phone is not None:
        user.phone = req.phone
    if req.email is not None:
        from app.models.user import User as UserModel
        exists = (
            db.query(UserModel)
            .filter(UserModel.email == req.email, UserModel.id != user.id)
            .first()
        )
        if exists:
            raise BizException(BizCode.EMAIL_ALREADY_EXISTS, http_status=409)
        user.email = req.email
    db.commit()
    db.refresh(user)
    return ok(
        data=UpdateMeData(
            userId=user.id,
            nickname=user.nickname,
            phone=user.phone,
            email=user.email,
        ).model_dump()
    )
