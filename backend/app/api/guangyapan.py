"""GuangYaPan drive proxy API."""

import base64
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_admin_id
from app.services.guangyapan_config_service import (
    decrypt_value,
    encrypt_value,
    get_config,
    get_or_create_config,
)
from app.services.guangyapan_service import GuangYaPanClient, GuangYaPanError
from database.core import get_db_session
from database.models import DriveFile

router = APIRouter(prefix="/api/drives/guangyapan", tags=["光鸭盘"])


class DriveRequest(BaseModel):
    # Optional for normal operations; the singleton DB config is used when omitted.
    access_token: str | None = Field(None, min_length=20)
    refresh_token: str | None = None
    client_id: str | None = None
    device_id: str | None = None


class ListRequest(DriveRequest):
    parent_id: str = ""
    page_size: int = Field(100, ge=1, le=1000)
    order_by: int = 3
    sort_type: int = 1


class FileActionRequest(DriveRequest):
    file_id: str = Field(..., min_length=1)


class FilesActionRequest(DriveRequest):
    file_ids: list[str] = Field(..., min_length=1)
    parent_id: str = ""


class MkdirRequest(DriveRequest):
    parent_id: str = ""
    name: str = Field(..., min_length=1)


class RenameRequest(FileActionRequest):
    name: str = Field(..., min_length=1)


class OfflineCreateRequest(DriveRequest):
    url: str = Field(..., min_length=1)
    parent_id: str = ""
    name: str | None = None


class OfflineListRequest(DriveRequest):
    task_ids: list[str] = Field(default_factory=list)
    statuses: list[int] = Field(default_factory=list)
    cursor: str = ""
    page_size: int = Field(100, ge=1, le=1000)


class OfflineDeleteRequest(DriveRequest):
    task_ids: list[str] = Field(..., min_length=1)


class UploadSessionRequest(DriveRequest):
    parent_id: str = ""
    name: str = Field(..., min_length=1)
    size: int = Field(..., ge=0)


class SaveUrlRequest(DriveRequest):
    url: str = Field(..., min_length=1)
    mode: Literal["offline", "upload"]
    parent_id: str = ""
    name: str | None = None


class UploadBytesRequest(DriveRequest):
    """上传 base64 编码的文件字节到光鸭云盘（用于密文/加密内容）"""
    file_data: str = Field(..., min_length=1, description="base64 编码的文件内容")
    name: str = Field(..., min_length=1, description="文件名（含扩展名）")
    parent_id: str = ""


class GuangYaPanConfigUpdate(BaseModel):
    access_token: str | None = Field(None, min_length=20)
    refresh_token: str | None = None
    client_id: str | None = None
    device_id: str | None = None
    default_parent_id: str | None = None


def _decrypt_config_value(encrypted: str | None) -> str | None:
    """解密存储的令牌；密文不可读时返回 400 而非 500。

    secret_key 轮换后旧密文无法解密，应提示调用方重新配置 Token，
    而不是抛出未处理的服务器错误。
    """
    if not encrypted:
        return None
    try:
        return decrypt_value(encrypted)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=400,
            detail="光鸭云盘配置密文无法解密，请重新配置 access_token / refresh_token",
        ) from exc


async def client_for(data: DriveRequest, db: AsyncSession) -> GuangYaPanClient:
    config = await get_config(db)
    access_token = data.access_token or _decrypt_config_value(config.AccessTokenEncrypted if config else None)
    if not access_token:
        raise HTTPException(status_code=400, detail="未配置光鸭云盘 access_token")
    refresh_token = data.refresh_token or _decrypt_config_value(config.RefreshTokenEncrypted if config else None)
    return GuangYaPanClient(
        access_token,
        refresh_token=refresh_token,
        client_id=data.client_id or (config.ClientId if config else None),
        device_id=data.device_id or (config.DeviceId if config else None),
    )


async def execute(data: DriveRequest, db: AsyncSession, operation):
    config = await get_config(db)
    client = await client_for(data, db)
    try:
        return await operation(client)
    except GuangYaPanError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    finally:
        if config:
            # GuangYaPan may rotate both tokens during refresh; keep the
            # singleton configuration usable for the next operation.
            config.AccessTokenEncrypted = encrypt_value(client.access_token)
            if client.refresh_token:
                config.RefreshTokenEncrypted = encrypt_value(client.refresh_token)
            await db.flush()
        await client.close()


async def default_parent_id(db: AsyncSession, supplied: str) -> str:
    if supplied:
        return supplied
    config = await get_config(db)
    if not config:
        return ""
    return config.DefaultParentId or ""


@router.get("/config")
async def get_guangyapan_config(_: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    config = await get_config(db)
    return {
        "configured": bool(config and config.AccessTokenEncrypted),
        "has_refresh_token": bool(config and config.RefreshTokenEncrypted),
        "client_id": config.ClientId if config else None,
        "device_id": config.DeviceId if config else None,
        "default_parent_id": (config.DefaultParentId or "") if config else "",
        "updated_at": config.UpdatedAt if config else None,
    }


@router.put("/config")
async def update_guangyapan_config(
    data: GuangYaPanConfigUpdate,
    _: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
):
    config = await get_or_create_config(db)
    fields = data.model_fields_set
    if "access_token" in fields:
        config.AccessTokenEncrypted = encrypt_value(data.access_token)
    if "refresh_token" in fields:
        config.RefreshTokenEncrypted = encrypt_value(data.refresh_token)
    if "client_id" in fields:
        config.ClientId = data.client_id.strip() if data.client_id else None
    if "device_id" in fields:
        config.DeviceId = data.device_id.strip() if data.device_id else None
    if "default_parent_id" in fields:
        config.DefaultParentId = (data.default_parent_id or "").strip()
    await db.flush()
    return await get_guangyapan_config(_, db)


class GuangYaPanTestRequest(DriveRequest):
    default_parent_id: str = ""


@router.post("/test")
async def test_guangyapan(
    data: GuangYaPanTestRequest,
    _: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
):
    """测试光鸭云盘凭据与默认目录 ID 是否可用。

    表单传入的 token 优先；留空时回退已存储的配置。
    通过列目录（最多 5 条）验证权限与目录存在性。
    """
    parent_id = (data.default_parent_id or "").strip()
    client = await client_for(data, db)
    try:
        result = await client.list_files(parent_id, page_size=5)
        items = result.get("list") or []
        sample = []
        for item in items[:5]:
            sample.append({
                "name": str(item.get("name") or item.get("fileName") or ""),
                "is_dir": bool(item.get("isDir") or item.get("is_dir") or item.get("dirType")),
            })
        return {
            "ok": True,
            "parent_id": parent_id,
            "total": result.get("total") or len(items),
            "sample": sample,
        }
    except GuangYaPanError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"光鸭云盘目录测试失败：{exc}",
        ) from exc
    finally:
        await client.close()


@router.post("/list")
async def list_files(data: ListRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    return await execute(data, db, lambda client: client.list_files(data.parent_id, data.page_size, data.order_by, data.sort_type))


@router.post("/download-url")
async def download_url(data: FileActionRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    return await execute(data, db, lambda client: client.download_url(data.file_id))


@router.post("/mkdir")
async def mkdir(data: MkdirRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    return await execute(data, db, lambda client: client.mkdir(data.parent_id, data.name))


@router.post("/rename")
async def rename(data: RenameRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    return await execute(data, db, lambda client: client.rename(data.file_id, data.name))


@router.post("/delete")
async def delete(data: FilesActionRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    return await execute(data, db, lambda client: client.delete(data.file_ids))


@router.post("/move")
async def move(data: FilesActionRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    return await execute(data, db, lambda client: client.move(data.file_ids, data.parent_id))


@router.post("/copy")
async def copy(data: FilesActionRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    return await execute(data, db, lambda client: client.copy(data.file_ids, data.parent_id))


@router.post("/offline/create")
async def offline_create(data: OfflineCreateRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    parent_id = await default_parent_id(db, data.parent_id)
    return await execute(data, db, lambda client: client.create_offline_task(data.url, parent_id, data.name))


@router.post("/offline/list")
async def offline_list(data: OfflineListRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    return await execute(data, db, lambda client: client.list_offline_tasks(data.task_ids, data.statuses, data.cursor, data.page_size))


@router.post("/offline/delete")
async def offline_delete(data: OfflineDeleteRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    return await execute(data, db, lambda client: client.delete_offline_tasks(data.task_ids))


@router.post("/upload/session")
async def upload_session(data: UploadSessionRequest, _: int = Depends(get_admin_id), db: AsyncSession = Depends(get_db_session)):
    parent_id = await default_parent_id(db, data.parent_id)
    return await execute(data, db, lambda client: client.upload_session(parent_id, data.name, data.size))


@router.post("/save-url")
async def save_url(
    data: SaveUrlRequest,
    _: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
):
    parent_id = await default_parent_id(db, data.parent_id)
    result = await execute(data, db, lambda client: client.save_url(data.url, data.mode, parent_id, data.name))
    record = await db.scalar(
        select(DriveFile).where(
            DriveFile.Provider == result.provider,
            DriveFile.ProviderFileId == result.file_id,
        )
    )
    if record is None:
        record = DriveFile(
            Provider=result.provider,
            ProviderFileId=result.file_id,
            SourceUrl=data.url,
            PlaybackUrl=result.url,
            Mode=result.mode,
            Name=result.name,
            Size=result.size,
            Status="ready",
        )
        db.add(record)
    else:
        record.SourceUrl = data.url
        record.PlaybackUrl = result.url
        record.Mode = result.mode
        record.Name = result.name
        record.Size = result.size
        record.Status = "ready"
        record.ErrorMessage = None
    await db.flush()
    return {
        "id": record.Id,
        "provider": result.provider,
        "provider_file_id": result.file_id,
        "url": result.url,
        "mode": result.mode,
        "name": result.name,
        "size": result.size,
        "status": record.Status,
    }


@router.post("/upload-bytes")
async def upload_bytes(
    data: UploadBytesRequest,
    _: int = Depends(get_admin_id),
    db: AsyncSession = Depends(get_db_session),
):
    """将 base64 编码的文件内容上传到光鸭云盘。

    适用于 URL 是密文/加密内容，无法通过后端直接下载的场景。
    Agent 可通过浏览器工具提取图片后，将 base64 数据提交此接口。
    """
    MAX_SIZE = 50 * 1024 * 1024  # 50 MB 上限
    try:
        content = base64.b64decode(data.file_data, validate=True)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"base64 解码失败: {exc}")
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail=f"文件过大: {len(content)} 字节，上限 {MAX_SIZE} 字节")

    parent_id = await default_parent_id(db, data.parent_id)

    async def _upload(client: GuangYaPanClient):
        return await client.upload_file_bytes(content, data.name, parent_id)

    result = await execute(data, db, _upload)

    record = await db.scalar(
        select(DriveFile).where(
            DriveFile.Provider == result.provider,
            DriveFile.ProviderFileId == result.file_id,
        )
    )
    if record is None:
        record = DriveFile(
            Provider=result.provider,
            ProviderFileId=result.file_id,
            SourceUrl=None,
            PlaybackUrl=result.url,
            Mode=result.mode,
            Name=result.name,
            Size=result.size,
            Status="ready",
        )
        db.add(record)
    else:
        record.PlaybackUrl = result.url
        record.Name = result.name
        record.Size = result.size
        record.Status = "ready"
        record.ErrorMessage = None
    await db.flush()
    return {
        "id": record.Id,
        "provider": result.provider,
        "provider_file_id": result.file_id,
        "url": result.url,
        "mode": result.mode,
        "name": result.name,
        "size": result.size,
        "status": record.Status,
    }
