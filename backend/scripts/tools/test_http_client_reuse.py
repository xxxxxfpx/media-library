"""测试 httpx.AsyncClient 复用 vs 不复用的性能对比"""

import asyncio
import httpx
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

import sqlite3
import base64
from typing import Tuple, List

from config import config

class WebDAVConfig:
    @property
    def username(self):
        return config.cloud_auth.username
    @property
    def password(self):
        return config.cloud_auth.password
    @property
    def prefix(self):
        return config.cloud_auth.prefix
    @property
    def basic_auth_token(self):
        return base64.b64encode(f"{self.username}:{self.password}".encode()).decode()

webdav_config = WebDAVConfig()

# ==================== 方案1: 不复用 (每次新建 AsyncClient) ====================
async def get_webdav_no_reuse(file_path: str) -> str:
    """不复用：每次创建新的 AsyncClient"""
    url = f'https://webdav.123pan.cn/webdav{webdav_config.prefix}/{file_path}'
    headers = {"Authorization": f"Basic {webdav_config.basic_auth_token}"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request("GET", url, headers=headers, follow_redirects=False)
        if response.status_code == 302:
            return response.headers.get("Location")
        raise Exception(f"status: {response.status_code}")

# ==================== 方案2: 复用 (共用一个 AsyncClient) ====================
_http_client = httpx.AsyncClient(timeout=30.0)

async def get_webdav_with_reuse(file_path: str) -> str:
    """复用：使用全局的 AsyncClient"""
    url = f'https://webdav.123pan.cn/webdav{webdav_config.prefix}/{file_path}'
    headers = {"Authorization": f"Basic {webdav_config.basic_auth_token}"}
    response = await _http_client.request("GET", url, headers=headers, follow_redirects=False)
    if response.status_code == 302:
        return response.headers.get("Location")
    raise Exception(f"status: {response.status_code}")

# ==================== 测试函数 ====================
async def test_no_reuse(file_path: str, num_requests: int) -> List[float]:
    """测试不复用的并发性能"""
    print(f"\n{'='*70}")
    print(f"方案1: 不复用 (每次新建 AsyncClient)")
    print(f"请求数: {num_requests}")
    print(f"{'='*70}\n")

    start = time.time()
    tasks = [get_webdav_no_reuse(file_path) for _ in range(num_requests)]
    await asyncio.gather(*tasks, return_exceptions=True)
    total_time = time.time() - start

    durations = [d for d in [time.time() - start] if d > 0]
    print(f"总耗时: {total_time*1000:.2f} ms")
    print(f"平均每请求: {total_time*1000/num_requests:.2f} ms")

    return [total_time]

async def test_with_reuse(file_path: str, num_requests: int) -> List[float]:
    """测试复用的并发性能"""
    print(f"\n{'='*70}")
    print(f"方案2: 复用 (共用 AsyncClient)")
    print(f"请求数: {num_requests}")
    print(f"{'='*70}\n")

    start = time.time()
    tasks = [get_webdav_with_reuse(file_path) for _ in range(num_requests)]
    await asyncio.gather(*tasks, return_exceptions=True)
    total_time = time.time() - start

    print(f"总耗时: {total_time*1000:.2f} ms")
    print(f"平均每请求: {total_time*1000/num_requests:.2f} ms")

    return [total_time]

async def test_single_request(file_path: str, name: str, func) -> float:
    """测试单个请求"""
    start = time.time()
    try:
        await func(file_path)
    except Exception as e:
        print(f"  Error: {e}")
    return time.time() - start

async def main():
    file_id = 49337

    # 从数据库获取 file_path
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'database', 'media.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT Id, Path FROM Files WHERE Id = {file_id}")
    row = cursor.fetchone()
    conn.close()

    if not row:
        print(f"文件 ID {file_id} 不存在")
        return

    file_id_db, file_path = row
    print(f"{'='*70}")
    print(f"httpx.AsyncClient 复用 vs 不复用 性能测试")
    print(f"{'='*70}")
    print(f"文件 ID: {file_id_db}")
    print(f"文件路径: {file_path}")

    # 单次请求测试（确认连通性）
    print(f"\n{'='*70}")
    print("单次请求测试")
    print(f"{'='*70}")

    print("方案1 (不复用):")
    duration = await test_single_request(file_path, "no_reuse", get_webdav_no_reuse)
    print(f"  耗时: {duration*1000:.2f} ms")

    print("方案2 (复用):")
    duration = await test_single_request(file_path, "reuse", get_webdav_with_reuse)
    print(f"  耗时: {duration*1000:.2f} ms")

    # 正式测试：10个并发请求
    num_requests = 10

    time_no_reuse = await test_no_reuse(file_path, num_requests)
    time_with_reuse = await test_with_reuse(file_path, num_requests)

    # 对比结果
    print(f"\n{'='*70}")
    print(f"性能对比总结 ({num_requests} 个并发请求)")
    print(f"{'='*70}")
    print(f"方案1 (不复用): {time_no_reuse[0]*1000:.2f} ms")
    print(f"方案2 (复用):   {time_with_reuse[0]*1000:.2f} ms")

    if time_with_reuse[0] < time_no_reuse[0]:
        speedup = time_no_reuse[0] / time_with_reuse[0]
        print(f"复用加速比: {speedup:.2f}x")
        print(f"节省时间:  {(time_no_reuse[0] - time_with_reuse[0])*1000:.2f} ms ({(1 - time_with_reuse[0]/time_no_reuse[0])*100:.1f}%)")
    else:
        print("复用效果不明显")

    # 清理
    await _http_client.aclose()

if __name__ == "__main__":
    asyncio.run(main())
