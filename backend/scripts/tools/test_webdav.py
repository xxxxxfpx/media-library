import asyncio
import httpx
from urllib.parse import quote
from config import config


async def main():
    headers = {"Authorization": f"Basic {config.cloud_auth.basic_auth_token}"}

    # 测试1: 根路径
    print("=== 测试1: WebDAV 根路径 ===")
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.request("GET", "https://webdav.123pan.cn/webdav/", headers=headers, follow_redirects=False)
        url = r.headers.get("Location", "N/A")[:80] if r.status_code == 302 else "N/A"
        print(f"Status: {r.status_code}, Location: {url}")

    # 测试2: prefix 路径
    print("=== 测试2: Prefix 路径 ===")
    encoded_prefix = quote(config.cloud_auth.prefix)
    url2 = f"https://webdav.123pan.cn/webdav{encoded_prefix}/"
    print(f"URL: {url2}")
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.request("GET", url2, headers=headers, follow_redirects=False)
        url = r.headers.get("Location", "N/A")[:80] if r.status_code == 302 else "N/A"
        print(f"Status: {r.status_code}, Location: {url}")


asyncio.run(main())
