"""测试 WebDAV 请求的并发性能"""

import asyncio
import httpx
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

import sqlite3
import base64
from typing import Tuple

# 导入项目配置
from config import config

class WebDAVConfig:
    """简化版配置，直接从 config 读取"""
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

async def get_webdav_redirect_url(file_path: str) -> str:
    """获取 WebDAV 重定向 URL（无缓存）"""
    url = f'https://webdav.123pan.cn/webdav{webdav_config.prefix}/{file_path}'
    headers = {"Authorization": f"Basic {webdav_config.basic_auth_token}"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request("GET", url, headers=headers, follow_redirects=False)
        if response.status_code == 302:
            return response.headers.get("Location")
        raise Exception(f"WebDAV 路径 {file_path} 未返回重定向, status: {response.status_code}")

async def single_request(file_path: str, request_id: int) -> Tuple[int, float, float, str]:
    """单个请求，记录开始和结束时间"""
    start_time = time.time()
    try:
        url = await get_webdav_redirect_url(file_path)
        end_time = time.time()
        return (request_id, start_time, end_time, "OK")
    except Exception as e:
        end_time = time.time()
        return (request_id, start_time, end_time, f"Error: {str(e)[:40]}")

async def test_concurrent_requests(file_path: str, num_requests: int = 10):
    """并发发起多个请求"""
    print(f"{'='*70}")
    print(f"并发测试: {num_requests} 个请求同时发起")
    print(f"文件路径: {file_path}")
    print(f"{'='*70}\n")

    total_start = time.time()

    tasks = [single_request(file_path, i) for i in range(num_requests)]
    results = await asyncio.gather(*tasks)

    total_end = time.time()

    print(f"{'请求ID':<8} {'相对开始(ms)':<14} {'相对结束(ms)':<14} {'耗时(ms)':<12} {'状态'}")
    print("-" * 70)

    for req_id, start, end, status in sorted(results, key=lambda x: x[0]):
        duration_ms = (end - start) * 1000
        elapsed_from_start = (start - total_start) * 1000
        print(f"{req_id:<8} {elapsed_from_start:<14.2f} {(end-total_start)*1000:<14.2f} {duration_ms:<12.2f} {status}")

    print("-" * 70)

    single_durations = [r[2] - r[1] for r in results]
    total_duration = total_end - total_start

    print(f"\n{'='*70}")
    print("性能统计")
    print("=" * 70)
    print(f"总耗时:           {total_duration*1000:.2f} ms")
    print(f"单请求平均耗时:   {sum(single_durations)/len(single_durations)*1000:.2f} ms")
    print(f"单请求最大耗时:   {max(single_durations)*1000:.2f} ms")
    print(f"单请求最小耗时:   {min(single_durations)*1000:.2f} ms")
    print(f"理论串行总耗时:   {sum(single_durations)*1000:.2f} ms")
    print(f"并发加速比:       {sum(single_durations) / total_duration:.2f}x")

    print(f"\n{'='*70}")
    print("并发效果分析")
    print("=" * 70)

    start_times = [r[1] for r in results]
    time_spread = max(start_times) - min(start_times)

    if time_spread < 0.2:
        print(f"✓ 请求几乎同时开始 (time_spread={time_spread*1000:.2f}ms)")
    else:
        print(f"✗ 请求开始有时间差: {time_spread*1000:.2f}ms")

    if total_duration < max(single_durations) * 1.5:
        print(f"✓ 总耗时接近单个请求最大耗时 - 真并发!")
    elif total_duration < sum(single_durations) * 0.5:
        print(f"✓ 总耗时远小于串行时间 - 有效并发!")
    else:
        print(f"✗ 并发效果不明显，可能有串行等待")

    # 检查是否所有请求几乎同时结束
    end_times = [r[2] for r in results]
    end_spread = max(end_times) - min(end_times)
    if end_spread < 0.5:
        print(f"✓ 请求几乎同时完成 (end_spread={end_spread*1000:.2f}ms)")
    else:
        print(f"  请求完成时间差: {end_spread*1000:.2f}ms")

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
    print(f"数据库查询: ID={file_id_db}")
    print(f"文件路径: {file_path}")
    print(f"WebDAV 配置: username={webdav_config.username}, prefix={webdav_config.prefix}")
    print()

    # 先测试单个请求确认连通性
    print("-" * 70)
    print("连通性测试 (单个请求)...")
    try:
        test_result = await single_request(file_path, 0)
        print(f"结果: {test_result[3]}, 耗时: {(test_result[2]-test_result[1])*1000:.2f}ms")
    except Exception as e:
        print(f"连接失败: {e}")
        return
    print("-" * 70)
    print()

    # 测试并发请求
    await test_concurrent_requests(file_path, num_requests=10)

if __name__ == "__main__":
    asyncio.run(main())
