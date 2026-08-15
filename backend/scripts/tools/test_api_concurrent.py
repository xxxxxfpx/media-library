"""测试 API 并发响应时间"""

import asyncio
import httpx
import time
import sys

API_URL = "http://localhost:5173/api/file/data?file_id=49337"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc3MzU4NzQzLCJ0eXBlIjoiYWNjZXNzIn0.OhK_ioCiwu0HG7Wb7qqyRaoIx0YEfYN2FTnS6jFbdUY"

async def single_request(session: httpx.AsyncClient, request_id: int) -> dict:
    """单个请求，记录开始和结束时间"""
    start_time = time.time()
    try:
        response = await session.get(API_URL, headers={"Authorization": f"Bearer {TOKEN}"}, follow_redirects=False)
        end_time = time.time()
        return {
                "id": request_id,
                "start": start_time,
                "end": end_time,
                "duration_ms": (end_time - start_time) * 1000,
                "status": response.status_code,
                "success": response.status_code in (302, 307)  # FastAPI RedirectResponse 返回 307
            }
    except Exception as e:
        end_time = time.time()
        return {
            "id": request_id,
            "start": start_time,
            "end": end_time,
            "duration_ms": (end_time - start_time) * 1000,
            "status": 0,
            "success": False,
            "error": str(e)[:50]
        }

async def test_concurrent_requests(num_requests: int = 16):
    """并发发送多个请求"""
    print(f"{'='*70}")
    print(f"并发测试: {num_requests} 个请求")
    print(f"API: {API_URL}")
    print(f"缓存: 已禁用 (强制 redirect_url=None)")
    print(f"{'='*70}\n")

    total_start = time.time()

    async with httpx.AsyncClient(timeout=60.0) as session:
        tasks = [single_request(session, i) for i in range(num_requests)]
        results = await asyncio.gather(*tasks)

    total_end = time.time()

    # 打印结果表格
    print(f"{'ID':<4} {'开始(ms)':<12} {'结束(ms)':<12} {'耗时(ms)':<12} {'状态':<6}")
    print("-" * 50)

    for r in sorted(results, key=lambda x: x["id"]):
        start_from_total = (r["start"] - total_start) * 1000
        end_from_total = (r["end"] - total_start) * 1000
        status_str = str(r["status"]) if r["success"] else f"Err({r.get('error', '?')[:20]})"
        print(f"{r['id']:<4} {start_from_total:<12.2f} {end_from_total:<12.2f} {r['duration_ms']:<12.2f} {status_str:<6}")

    print("-" * 50)

    # 统计
    durations = [r["duration_ms"] for r in results]
    successes = sum(1 for r in results if r["success"])

    print(f"\n{'='*70}")
    print("性能统计")
    print("=" * 70)
    print(f"总耗时:           {(total_end - total_start)*1000:.2f} ms")
    print(f"成功请求:         {successes}/{num_requests}")
    print(f"单请求耗时:       min={min(durations):.2f}ms, max={max(durations):.2f}ms, avg={sum(durations)/len(durations):.2f}ms")
    print(f"理论串行耗时:     {sum(durations):.2f} ms")
    print(f"并发加速比:       {sum(durations)/(total_end - total_start)/1000:.2f}x")

    print(f"\n{'='*70}")
    print("并发效果分析")
    print("=" * 70)

    # 分析开始时间
    start_times = [r["start"] for r in results]
    start_spread = (max(start_times) - min(start_times)) * 1000
    if start_spread < 100:
        print(f"✓ 请求几乎同时开始 (spread={start_spread:.2f}ms)")
    else:
        print(f"✗ 请求开始有时间差: {start_spread:.2f}ms")

    # 分析结束时间
    end_times = [r["end"] for r in results]
    end_spread = (max(end_times) - min(end_times)) * 1000
    if end_spread < 500:
        print(f"✓ 请求几乎同时完成 (spread={end_spread:.2f}ms)")
    else:
        print(f"  请求完成时间差: {end_spread:.2f}ms")

    # 分析总耗时
    if (total_end - total_start) < max(durations) / 1000 * 1.5:
        print("✓ 总耗时 ≈ 单请求最大耗时 - 真并发!")
    else:
        print(f"  总耗时: {(total_end - total_start)*1000:.2f}ms, 单请求最大: {max(durations):.2f}ms")

async def main():
    await test_concurrent_requests(num_requests=16)

if __name__ == "__main__":
    asyncio.run(main())