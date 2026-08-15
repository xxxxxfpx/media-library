"""用户 API 接口"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginRequest, LoginResponse, RefreshTokenRequest
from app.schemas.user import UserInfo, UpdateUserDataRequest
from app.schemas.setting import UserSettings, UpdateUserSettingsRequest
from app.services.auth_service import AuthService
from app.services.media_service import get_media_list
from app.services.user_service import update_userdata, get_user_setting, update_user_setting
from app.api.deps import get_current_user, get_user_id
from database.models import User
from database.core import get_db_session

router = APIRouter(prefix="/api/user", tags=["用户"])


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db_session)):
    user = await AuthService.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌载荷"
        )

    user = await AuthService.get_user_by_id(db, int(user_id))
    if not user or not user.IsActive:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已禁用"
        )

    access_token = AuthService.create_access_token(data={"sub": str(user.Id)})
    refresh_token = AuthService.create_refresh_token(data={"sub": str(user.Id)})

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
async def logout(user_id: int = Depends(get_user_id), current_user: User = Depends(get_current_user)):
    return {"message": "登出成功"}


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
