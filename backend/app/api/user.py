"""用户 API 接口"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, Request
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginRequest, LoginResponse, RefreshTokenRequest
from app.schemas.user import UserInfo, UpdateUserDataRequest, ChangePasswordRequest
from app.schemas.setting import UserSettings, UpdateUserSettingsRequest
from app.services.auth_service import AuthService
from app.services.media_service import get_media_list
from app.services.user_service import update_userdata, get_user_setting, update_user_setting, change_password
from app.services.rate_limiter import is_login_blocked, record_login_failure, reset_login_failures
from app.services.token_denylist import revoke_token, _payload_exp_ttl
from app.api.deps import get_current_user, get_user_id, security as app_deps_security
from database.models import User
from database.core import get_db_session

router = APIRouter(prefix="/api/user", tags=["用户"])

logger = logging.getLogger(__name__)


def _client_ip(request: Request) -> str:
    """提取客户端 IP（兼容反代转发）"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/login", response_model=LoginResponse)
async def login(request: Request, body: LoginRequest, db: AsyncSession = Depends(get_db_session)):
    ip = _client_ip(request)
    if is_login_blocked(ip, body.username):
        logger.warning("登录失败: 限流拦截 | ip=%s username=%s", ip, body.username)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="登录尝试过于频繁，请稍后再试",
        )

    user = await AuthService.authenticate_user(db, body.username, body.password)
    if not user:
        record_login_failure(ip, body.username)
        logger.warning("登录失败: 用户名或密码错误 | ip=%s username=%s", ip, body.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    reset_login_failures(ip, body.username)
    logger.info("登录成功 | user_id=%s username=%s ip=%s", user.Id, user.Name, ip)

    access_token = AuthService.create_access_token(data={"sub": str(user.Id)})
    refresh_token = AuthService.create_refresh_token(data={"sub": str(user.Id)})

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db_session)):
    payload = AuthService.decode_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        logger.warning("刷新令牌失败: 无效令牌")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )

    user_id = payload.get("sub")
    if not user_id:
        logger.warning("刷新令牌失败: 载荷缺少 sub")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌载荷"
        )

    user = await AuthService.get_user_by_id(db, int(user_id))
    if not user or not user.IsActive:
        logger.warning("刷新令牌失败: 用户不存在或已禁用 | user_id=%s", user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已禁用"
        )

    access_token = AuthService.create_access_token(data={"sub": str(user.Id)})
    refresh_token = AuthService.create_refresh_token(data={"sub": str(user.Id)})
    logger.info("刷新令牌成功 | user_id=%s", user.Id)

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get("/info", response_model=UserInfo)
async def get_user_info(user_id: int = Depends(get_user_id), current_user: User = Depends(get_current_user)):
    return UserInfo(
        id=current_user.Id,
        username=current_user.Name,
        email=current_user.Email,
        is_admin=current_user.IsAdmin,
        is_active=True,
        created_at=current_user.CreatedAt.isoformat() if current_user.CreatedAt else None,
    )


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(app_deps_security),
    user_id: int = Depends(get_user_id),
    current_user: User = Depends(get_current_user),
):
    """登出：将当前访问令牌加入 denylist，立即失效"""
    token = credentials.credentials
    payload = AuthService.decode_token(token)
    if payload:
        revoke_token(payload.get("jti"), _payload_exp_ttl(payload.get("exp")))
    logger.info("登出 | user_id=%s", user_id)

    return {"message": "登出成功"}


@router.post("/change-password")
async def api_change_password(
    body: ChangePasswordRequest,
    user_id: int = Depends(get_user_id),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """修改当前用户密码"""
    try:
        await change_password(db, user_id, body.old_password, body.new_password)
    except ValueError as e:
        logger.warning("修改密码失败: %s | user_id=%s", e, user_id)
        raise HTTPException(status_code=400, detail=str(e))
    logger.info("修改密码成功 | user_id=%s", user_id)
    # 修改密码后撤销当前令牌，强制重新登录
    return {"message": "密码修改成功，请重新登录"}


@router.post("/userdata")
async def api_update_userdata(
    request: UpdateUserDataRequest,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    return await update_userdata(db=db, user_id=user_id, request=request)


@router.get("/history")
async def get_history(
    limit: int = Query(60, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    return await get_media_list(
        db=db,
        user_id=user_id,
        has_playback=True,
        sort_by="date_created",
        limit=limit,
        offset=offset,
    )


@router.get("/setting", response_model=UserSettings)
async def api_get_user_setting(user_id: int = Depends(get_user_id), current_user: User = Depends(get_current_user)):
    return await get_user_setting(db=None, user=current_user)


@router.post("/setting", response_model=UserSettings)
async def api_update_user_setting(
    setting: UpdateUserSettingsRequest = Body(..., description="用户设置"),
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    return await update_user_setting(db=db, user_id=user_id, setting=setting)
