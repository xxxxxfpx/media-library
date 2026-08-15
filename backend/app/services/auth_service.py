"""
认证服务层
"""

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_config
from database.models import User

config = get_config()


class AuthService:
    """认证服务"""

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=config.jwt.access_token_expire_minutes))
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, config.app.secret_key, algorithm=config.jwt.algorithm)

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """创建刷新令牌"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=config.jwt.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, config.app.secret_key, algorithm=config.jwt.algorithm)

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """解码令牌"""
        try:
            payload = jwt.decode(token, config.app.secret_key, algorithms=[config.jwt.algorithm])
            return payload
        except JWTError:
            return None

    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
        """认证用户"""
        result = await db.execute(select(User).where(User.Name == username).limit(1))
        user = result.scalar_one_or_none()
        if not user or not user.verify_password(password):
            return None
        return user

    @staticmethod
    async def create_user(db: AsyncSession, username: str, password: str, email: str = None, is_admin: bool = False) -> User:
        """创建用户"""
        user = User(Name=username, Email=email, IsAdmin=is_admin)
        user.set_password(password)
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        result = await db.execute(select(User).where(User.Id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        result = await db.execute(select(User).where(User.Name == username).limit(1))
        return result.scalar_one_or_none()
