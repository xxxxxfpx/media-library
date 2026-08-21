"""
MaccmsClient - 苹果CMS V10 采集协议客户端
=============================================

封装苹果CMS provide/vod 接口，支持：
- 列表查询（ac=list, ac=videolist）
- 详情查询（ac=detail + ids）
- 增量采集（按小时参数 h）
- 批量详情（ids 逗号分隔）
- 播放地址解析（vod_play_from/vod_play_url）

超时策略：列表15s，详情15s，避免长时间阻塞。
"""

from __future__ import annotations

import logging
from typing import Any, Iterator

import requests

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 15
DEFAULT_HEADERS = {
    "User-Agent": "MediaLibrary-Collector/1.0",
    "Accept": "application/json, text/plain, */*",
}

# 每次 detail 批量请求的最大 ID 数，避免 URL 过长
_BATCH_DETAIL_SIZE = 30


class MaccmsError(Exception):
    """苹果CMS接口错误"""

    def __init__(self, message: str, status_code: int | None = None, response_text: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class MaccmsClient:
    """苹果CMS V10 协议客户端"""

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT):
        """初始化客户端。

        Args:
            base_url: API基础URL，如 https://155api.com/api.php/provide/vod/
            timeout: 请求超时秒数
        """
        self.base = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.s = requests.Session()
        self.s.headers.update(DEFAULT_HEADERS)

    def list(
        self,
        pg: int = 1,
        h: int | None = None,
        t: int | None = None,
        wd: str | None = None,
        at: str = "json",
    ) -> dict[str, Any]:
        """请求视频列表。

        Args:
            pg: 页码，从1开始
            h: 仅返回最近N小时更新的数据（增量采集）
            t: 分类ID
            wd: 关键词搜索
            at: 输出格式 json/xml

        Returns:
            解析后的JSON响应字典
        """
        params: dict[str, Any] = {"ac": "list", "pg": pg, "at": at}
        if h is not None:
            params["h"] = h
        if t is not None:
            params["t"] = t
        if wd:
            params["wd"] = wd
        return self._get(params)

    def detail(self, ids: int | str | list[int]) -> list[dict[str, Any]]:
        """请求视频详情（支持批量）。

        Args:
            ids: 视频ID，支持 int / "1,2,3" / [1,2,3]

        Returns:
            详情列表（取响应的 list 字段）
        """
        if isinstance(ids, (list, tuple)):
            ids_str = ",".join(str(i) for i in ids)
        else:
            ids_str = str(ids)

        result = self._get({"ac": "detail", "ids": ids_str})
        return result.get("list", [])

    def detail_batch(self, ids: list[int], batch_size: int = _BATCH_DETAIL_SIZE) -> list[dict[str, Any]]:
        """批量请求详情，自动分片。

        Args:
            ids: 视频ID列表
            batch_size: 每批最大ID数

        Returns:
            合并的详情列表
        """
        all_details: list[dict[str, Any]] = []
        for i in range(0, len(ids), batch_size):
            batch = ids[i : i + batch_size]
            try:
                details = self.detail(batch)
                all_details.extend(details)
            except MaccmsError:
                logger.warning("detail_batch: 批次 %d-%d 失败，跳过", i, i + len(batch))
        return all_details

    def iter_incremental(self, h: int | None = None, max_pages: int = 50) -> Iterator[dict[str, Any]]:
        """增量迭代器，自动翻页。

        Args:
            h: 仅最近N小时；None则全量
            max_pages: 最大翻页数（安全阀）

        Yields:
            每条 vod 列表记录的字典
        """
        pg = 1
        while pg <= max_pages:
            data = self.list(pg=pg, h=h)
            items = data.get("list", [])
            if not items:
                break
            yield from items
            pagecount = int(data.get("pagecount", 1))
            if pg >= pagecount:
                break
            pg += 1

    def parse_play_urls(self, vod_detail: dict[str, Any]) -> list[dict[str, Any]]:
        """解析 vod_play_from/vod_play_url 为结构化数据。

        苹果CMS格式：
        - vod_play_from: 多个源用 $$$ 分隔
        - vod_play_url: 对应每个源的集数列表，集内用 # 分隔，集名与URL用 $ 分隔

        Args:
            vod_detail: detail接口返回的单条vod数据

        Returns:
            播放源列表 [{source: str, episodes: [{name: str, url: str}]}]
        """
        play_from = vod_detail.get("vod_play_from", "")
        play_url = vod_detail.get("vod_play_url", "")

        if not play_from or not play_url:
            return []

        sources = play_from.split("$$$")
        urls = play_url.split("$$$")

        result: list[dict[str, Any]] = []
        for src, url_str in zip(sources, urls):
            episodes: list[dict[str, str]] = []
            for item in url_str.split("#"):
                if "$" in item:
                    name, url = item.split("$", 1)
                    episodes.append({"name": name.strip(), "url": url.strip()})
                else:
                    # 没有集名，直接当URL
                    episodes.append({"name": "", "url": item.strip()})
            result.append({"source": src, "episodes": episodes})
        return result

    def test_connection(self) -> dict[str, Any]:
        """测试采集源连通性。

        Returns:
            包含 code/msg/total/pagecount 的简单状态字典

        Raises:
            MaccmsError: 连接失败
        """
        data = self.list(pg=1)
        return {
            "code": data.get("code"),
            "msg": data.get("msg"),
            "total": data.get("total", 0),
            "pagecount": data.get("pagecount", 0),
            "list_count": len(data.get("list", [])),
        }

    def close(self) -> None:
        """关闭底层HTTP会话"""
        self.s.close()

    def _get(self, params: dict[str, Any]) -> dict[str, Any]:
        """发起GET请求并解析JSON。

        Raises:
            MaccmsError: 请求失败或解析失败
        """
        try:
            r = self.s.get(self.base, params=params, timeout=self.timeout, verify=False)
            r.raise_for_status()
            r.encoding = "utf-8"
            return r.json()
        except requests.exceptions.ConnectionError as e:
            raise MaccmsError(f"连接失败: {e}") from e
        except requests.exceptions.Timeout as e:
            raise MaccmsError(f"请求超时({self.timeout}s): {e}") from e
        except requests.exceptions.HTTPError as e:
            raise MaccmsError(
                f"HTTP错误 {r.status_code}: {e}",
                status_code=r.status_code,
                response_text=r.text[:500] if "r" in dir() else None,
            ) from e
        except (ValueError, requests.exceptions.RequestException) as e:
            raise MaccmsError(f"解析失败: {e}") from e

    def __enter__(self) -> "MaccmsClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
