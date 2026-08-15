"""测试 WebDAV 请求的并发性能 - 详细版"""

import asyncio
import httpx
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

import sqlite3
import base64
from typing import Tuple

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

async def get_webdav_redirect_url(file_path: str) -> str:
    url = f'https://webdav.123pan.cn/webdav{webdav_config.prefix}/{file_path}'
    headers = {"Authorization": f"Basic {webdav_config.basic_auth_token}"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request("GET", url, headers=headers, follow_redirects=False)
        if response.status_code == 302:
            return response.headers.get("Location")
        raise Exception(f"status: {response.status_code}")

async def single_request(file_path: str, request_id: int) -> Tuple[int, float, float, str]:
    start_time = time.time()
    try:
        url = await get_webdav_redirect_url(file_path)
        end_time = time.time()
        return (request_id, start_time, end_time, "OK")
    except Exception as e:
        end_time = time.time()
        return (request_id, start_time, end_time, f"Error")

async def test_with_creation_delay(file_path: str, num_requests: int = 10):
    """测试：任务创建后立即执行 vs 等待一小段时间"""
    print(f"\n{'='*70}")
    print(f"测试2: asyncio.gather 任务创建时机分析")
    print(f"{'='*70}\n")

    # 方法1：先创建所有任务，再 gather
    print("方法1: 先创建所有任务，再 gather")
    print("-" * 40)
    total_start = time.time()

    # 记录任务创建时间
    task_creation_times = []
    tasks = []
    for i in range(num_requests):
        task_start = time.time()
        task = asyncio.create_task(single_request(file_path, i))
        tasks.append(task)
        task_creation_times.append(time.time() - total_start)

    print(f"任务创建完成，耗时: {(time.time() - total_start)*1000:.2f}ms")
    for i, t in enumerate(task_creation_times):
        print(f"  任务 {i} 创建于: {t*1000:.2f}ms")

    results = await asyncio.gather(*tasks)
    total_end = time.time()

    print(f"\n所有任务完成，总耗时: {(total_end - total_start)*1000:.2f}ms")

    # 分析
    print(f"\n{'='*70}")
    print("分析:")
    print("=" * 70)

    start_times = [r[1] - total_start for r in results]
    print(f"任务开始时间范围: {min(start_times)*1000:.2f}ms ~ {max(start_times)*1000:.2f}ms")
    print(f"任务创建时间范围: {min(task_creation_times)*1000:.2f}ms ~ {max(task_creation_times)*1000:.2f}ms")
    print(f"任务创建总耗时: {task_creation_times[-1]*1000:.2f}ms")

    end_times = [r[2] - total_start for r in results]
    print(f"任务结束时间范围: {min(end_times)*1000:.2f}ms ~ {max(end_times)*1000:.2f}ms")
    print(f"结束时间差: {(max(end_times) - min(end_times))*1000:.2f}ms")

async def test_true_concurrent(file_path: str, num_requests: int = 10):
    """真正的并发测试：确保所有任务同时开始"""
    print(f"\n{'='*70}")
    print(f"测试3: 真正的并发测试")
    print(f"{'='*70}\n")

    # 创建所有任务
    tasks = [asyncio.create_task(single_request(file_path, i)) for i in range(num_requests)]

    # 短暂等待确保任务都在运行
    await asyncio.sleep(0.001)

    total_start = time.time()
    results = await asyncio.gather(*tasks)
    total_end = time.time()

    print(f"总耗时: {(total_end - total_start)*1000:.2f}ms")

    durations = [r[2] - r[1] for r in results]
    print(f"单请求耗时: min={min(durations)*1000:.2f}ms, max={max(durations)*1000:.2f}ms, avg={sum(durations)/len(durations)*1000:.2f}ms")

    return total_end - total_start

async def test_sequential(file_path: str, num_requests: int = 5):
    """串行测试作为对比"""
    print(f"\n{'='*70}")
    print(f"串行测试（对比）: {num_requests} 个请求顺序执行")
    print(f"{'='*70}\n")

    total_start = time.time()
    results = []
    for i in range(num_requests):
        result = await single_request(file_path, i)
        results.append(result)
        print(f"请求 {i} 完成，耗时: {(result[2]-result[1])*1000:.2f}ms")

    total_end = time.time()
    print(f"\n串行总耗时: {(total_end - total_start)*1000:.2f}ms")
    return total_end - total_start

async def main():
    file_id = 49337

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
    print(f"文件 ID: {file_id_db}")
    print(f"文件路径: {file_path}")

    # 连通性测试
    print("\n" + "-"*70)
    print("连通性测试...")
    test_result = await single_request(file_path, 0)
    print(f"结果: {test_result[3]}, 耗时: {(test_result[2]-test_result[1])*1000:.2f}ms")

    # 并发测试
    concurrent_time = await test_true_concurrent(file_path, num_requests=10)

    # 串行测试
    sequential_time = await test_sequential(file_path, num_requests=5)

    # 对比
    print(f"\n{'='*70}")
    print("性能对比")
    print("=" * 70)
    print(f"5个串行请求耗时: {sequential_time*1000:.2f}ms")
    print(f"10个并发请求耗时: {concurrent_time*1000:.2f}ms")
    print(f"理论并发加速比: {sequential_time * 2 / concurrent_time:.2f}x")

    if concurrent_time < sequential_time * 0.6:
        print("\n✓ 确认：并发请求比串行快得多，确实是并发执行！")
    else:
        print("\n? 并发效果不明显，可能需要进一步分析")

if __name__ == "__main__":
    asyncio.run(main())
