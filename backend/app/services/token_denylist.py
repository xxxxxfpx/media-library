"""令牌注销列表（denylist）- 基于 diskcache

登出后将 token 的 jti 写入 denylist，TTL 为令牌剩余有效时间，
使已登出的访问令牌立即失效（即使未过期）。
"""

import os
import time

import diskcache

_cache_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "cache", "token_denylist",
)
os.makedirs(_cache_dir, exist_ok=True)

_denylist = diskcache.Cache(_cache_dir)


def revoke_token(jti: str, ttl_seconds: int) -> None:
    """注销令牌：写入 denylist，TTL 为剩余有效时间（至少 1 秒）"""
    if not jti:
        return
    _denylist.set(f"revoked_{jti}", True, expire=max(int(ttl_seconds), 1))


def is_token_revoked(jti: str) -> bool:
    """检查令牌是否已注销"""
    if not jti:
        return False
    return _denylist.get(f"revoked_{jti}") is not None


def _payload_exp_ttl(exp: float | int | None) -> int:
    """根据 exp 计算剩余 TTL 秒数"""
    if not exp:
        return 86400  # 默认 1 天
    try:
        remaining = int(exp) - int(time.time())
        return max(remaining, 1)
    except (TypeError, ValueError):
        return 86400
