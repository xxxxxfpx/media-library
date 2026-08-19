"""Persistence and encryption helpers for the singleton GuangYaPan config."""

import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from database.models import GuangYaPanConfig


def _cipher() -> Fernet:
    key = base64.urlsafe_b64encode(hashlib.sha256(config.app.secret_key.encode("utf-8")).digest())
    return Fernet(key)


def encrypt_value(value: str | None) -> str | None:
    if not value:
        return None
    return _cipher().encrypt(value.strip().encode("utf-8")).decode("ascii")


def decrypt_value(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return _cipher().decrypt(value.encode("ascii")).decode("utf-8")
    except (InvalidToken, ValueError) as exc:
        raise RuntimeError("光芽云盘配置密文无法解密，请重新配置 Token") from exc


async def get_config(db: AsyncSession) -> GuangYaPanConfig | None:
    return await db.scalar(select(GuangYaPanConfig).where(GuangYaPanConfig.Id == 1))


async def get_or_create_config(db: AsyncSession) -> GuangYaPanConfig:
    record = await get_config(db)
    if record is None:
        record = GuangYaPanConfig(Id=1)
        db.add(record)
        await db.flush()
    return record
