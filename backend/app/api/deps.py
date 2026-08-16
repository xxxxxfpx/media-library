"""API 依赖项"""

from typing import Optional
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth_service import AuthService
from app.services.token_denylist import is_token_revoked
from database.models import User
from database.core import get_db_session

security = HTTPBearer(auto_error=False)


def _validate_payload(payload) -> None:
    """校验令牌载荷并检查 denylist（登出后立即失效）"""
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌类型",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if is_token_revoked(payload.get("jti")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌已失效",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌载荷",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """从请求头提取并校验 token，返回 user_id"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials

    payload = AuthService.decode_token(token)
    _validate_payload(payload)

    return int(payload["sub"])


async def get_current_user(
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    user = await AuthService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.IsActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )

    return user


async def get_optional_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[int]:
    """可选获取 user_id（未认证返回 None）"""
    if not credentials:
        return None
    token = credentials.credentials
    payload = AuthService.decode_token(token)
    if not payload or payload.get("type") != "access":
        return None
    if is_token_revoked(payload.get("jti")):
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    return int(user_id)


async def get_user_id_from_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    token: Optional[str] = Query(None, description="访问令牌（兼容无 Header 的媒体加载场景）"),
    db: AsyncSession = Depends(get_db_session),
) -> int:
    """从 Bearer 请求头或 token 查询参数校验令牌，返回 user_id

    浏览器 `<img>`/`<video>` 以及 Flutter `Image.network` 等媒体加载无法携带
    Authorization 请求头，需通过 query 参数附带令牌。
    """
    raw = None
    if credentials:
        raw = credentials.credentials
    elif token:
        raw = token

    if not raw:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = AuthService.decode_token(raw)
    _validate_payload(payload)

    user_id = int(payload["sub"])

    # 校验用户仍存在且激活：已删除/禁用用户的媒体 URL 立即失效
    user = await AuthService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.IsActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )

    return user_id


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """校验当前用户是否为管理员"""
    if not current_user.IsAdmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user


async def get_admin_id(
    current_user: User = Depends(get_current_admin),
) -> int:
    """获取当前管理员用户 ID"""
    return current_user.Id
