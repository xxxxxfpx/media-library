"""GuangYaPan API client based on the OpenList GuangYaPan driver."""

from __future__ import annotations

import asyncio
import hashlib
import os
import tempfile
from typing import Any

import httpx
import oss2

from app.services.drive_contracts import SavedFile, SaveMode

ACCOUNT_BASE_URL = "https://account.guangyapan.com"
API_BASE_URL = "https://api.guangyapan.com"


class GuangYaPanError(RuntimeError):
    pass


class GuangYaPanClient:
    def __init__(
        self,
        access_token: str,
        *,
        refresh_token: str | None = None,
        client_id: str | None = None,
        device_id: str | None = None,
    ):
        self.access_token = access_token.strip()
        self.refresh_token = (refresh_token or "").strip()
        if not self.access_token:
            raise ValueError("access_token is required")
        self.device_id = (device_id or "").strip() or "0123456789abcdef0123456789abcdef"
        self.client_id = (client_id or "").strip() or "aMe-8VSlkrbQXpUR"
        self.client = httpx.AsyncClient(
            base_url=API_BASE_URL,
            timeout=httpx.Timeout(30.0, connect=10.0),
            headers={
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
                "Did": self.device_id,
                "Dt": "4",
            },
        )

    async def refresh_access_token(self) -> dict[str, Any]:
        if not self.refresh_token:
            raise GuangYaPanError("refresh_token is required")
        async with httpx.AsyncClient(base_url=ACCOUNT_BASE_URL, timeout=30.0) as client:
            response = await client.post(
                "/v1/auth/token",
                json={
                    "client_id": self.client_id,
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                },
            )
            if response.status_code >= 400:
                raise GuangYaPanError(f"refresh status={response.status_code}: {response.text[:500]}")
            data = response.json()
        token = str(data.get("access_token") or "").strip()
        if not token:
            raise GuangYaPanError(str(data.get("error_description") or data.get("error") or "refresh returned no access_token"))
        self.access_token = token
        self.refresh_token = str(data.get("refresh_token") or self.refresh_token).strip()
        self.client.headers["Authorization"] = f"Bearer {self.access_token}"
        return data

    async def validate_account_token(self) -> dict[str, Any]:
        """Validate the supplied token against the account service.

        Account JWTs and resource API access tokens are not interchangeable;
        this method makes that distinction explicit for callers.
        """
        async with httpx.AsyncClient(base_url=ACCOUNT_BASE_URL, timeout=30.0) as client:
            response = await client.get(
                "/v1/user/me",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            if response.status_code >= 400:
                raise GuangYaPanError(f"account token status={response.status_code}: {response.text[:500]}")
            return response.json()

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self) -> GuangYaPanClient:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def post(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        response = await self.client.post(path, json=body or {})
        if response.status_code in {401, 403} and self.refresh_token:
            await self.refresh_access_token()
            response = await self.client.post(path, json=body or {})
        if response.status_code >= 400:
            raise GuangYaPanError(f"upstream status={response.status_code}: {response.text[:500]}")
        try:
            data = response.json()
        except ValueError as exc:
            raise GuangYaPanError("upstream returned invalid JSON") from exc
        msg = str(data.get("msg") or "").strip()
        if msg and msg.lower() != "success":
            raise GuangYaPanError(msg)
        return data

    async def list_files(self, parent_id: str = "", page_size: int = 100, order_by: int = 3, sort_type: int = 1) -> dict[str, Any]:
        page = 0
        result: list[dict[str, Any]] = []
        total = 0
        while True:
            data = await self.post("/userres/v1/file/get_file_list", {
                "parentId": parent_id,
                "page": page,
                "pageSize": max(1, min(page_size, 1000)),
                "orderBy": order_by,
                "sortType": sort_type,
            })
            payload = data.get("data") or {}
            entries = payload.get("list") or []
            result.extend(entries)
            total = payload.get("total") or total
            if len(entries) < page_size or (total and len(result) >= total):
                break
            page += 1
        return {"total": total or len(result), "list": result}

    async def download_url(self, file_id: str) -> dict[str, Any]:
        data = await self.post("/nd.bizuserres.s/v1/get_res_download_url", {"fileId": file_id})
        payload = data.get("data") or {}
        return {
            "file_id": file_id,
            "url": payload.get("signedURL") or payload.get("downloadUrl"),
        }

    async def mkdir(self, parent_id: str, name: str) -> dict[str, Any]:
        return await self.post("/nd.bizuserres.s/v1/file/create_dir", {"parentId": parent_id, "dirName": name})

    async def rename(self, file_id: str, name: str) -> dict[str, Any]:
        return await self.post("/nd.bizuserres.s/v1/file/rename", {"fileId": file_id, "newName": name})

    async def delete(self, file_ids: list[str]) -> dict[str, Any]:
        data = await self.post("/nd.bizuserres.s/v1/file/delete_file", {"fileIds": file_ids})
        task_id = str((data.get("data") or {}).get("taskId") or "")
        if task_id:
            await self.wait_task(task_id)
        return data

    async def move(self, file_ids: list[str], parent_id: str) -> dict[str, Any]:
        data = await self.post("/nd.bizuserres.s/v1/file/move_file", {"fileIds": file_ids, "parentId": parent_id})
        task_id = str((data.get("data") or {}).get("taskId") or "")
        if task_id:
            await self.wait_task(task_id)
        return data

    async def copy(self, file_ids: list[str], parent_id: str) -> dict[str, Any]:
        data = await self.post("/nd.bizuserres.s/v1/file/copy_file", {"fileIds": file_ids, "parentId": parent_id})
        task_id = str((data.get("data") or {}).get("taskId") or "")
        if task_id:
            await self.wait_task(task_id)
        return data

    async def create_offline_task(self, url: str, parent_id: str = "", name: str | None = None) -> dict[str, Any]:
        resolved = await self.post("/cloudcollection/v1/resolve_res", {"url": url})
        resolved_data = resolved.get("data") or {}
        task_url = resolved_data.get("url") or url
        task_name = self._source_file_name(url)
        payload = {"url": task_url, "parentId": parent_id, "newName": task_name}
        bt_info = resolved_data.get("btResInfo") or {}
        indexes = [item.get("fileIndex", index) for index, item in enumerate(bt_info.get("subfiles") or [])]
        if indexes:
            payload["fileIndexes"] = indexes
        created = await self.post("/cloudcollection/v1/create_task", payload)
        return created.get("data") or created

    async def wait_offline_file(self, task_id: str, timeout: float = 1800.0) -> dict[str, Any]:
        deadline = asyncio.get_running_loop().time() + timeout
        while asyncio.get_running_loop().time() < deadline:
            result = await self.list_offline_tasks([task_id], page_size=10)
            tasks = result.get("list") or []
            task = tasks[0] if tasks else None
            if task:
                file_id = str(task.get("fileId") or "").strip()
                status = task.get("status")
                if file_id:
                    return task
                if status in {-1, 3}:
                    raise GuangYaPanError(f"offline task failed: {task_id}, status={status}")
            await asyncio.sleep(2)
        raise GuangYaPanError(f"offline task timeout: {task_id}")

    async def list_offline_tasks(self, task_ids: list[str] | None = None, statuses: list[int] | None = None, cursor: str = "", page_size: int = 100) -> dict[str, Any]:
        payload: dict[str, Any] = {"pageSize": page_size}
        if task_ids:
            payload["taskIds"] = task_ids
        if statuses:
            payload["status"] = statuses
        if cursor:
            payload["cursor"] = cursor
        data = await self.post("/cloudcollection/v1/list_task", payload)
        return data.get("data") or {}

    async def delete_offline_tasks(self, task_ids: list[str]) -> dict[str, Any]:
        return await self.post("/cloudcollection/v2/delete_task", {"taskIds": task_ids})

    async def wait_task(self, task_id: str, timeout: float = 30.0) -> dict[str, Any]:
        deadline = asyncio.get_running_loop().time() + timeout
        while asyncio.get_running_loop().time() < deadline:
            data = await self.post("/nd.bizuserres.s/v1/get_task_status", {"taskId": task_id})
            status = (data.get("data") or {}).get("status")
            if status == 2:
                return data
            if status in {-1, 3}:
                raise GuangYaPanError(f"task failed: {task_id}, status={status}")
            await asyncio.sleep(0.3)
        raise GuangYaPanError(f"task timeout: {task_id}")

    async def upload_session(self, parent_id: str, name: str, size: int) -> dict[str, Any]:
        """Return GuangYaPan's temporary OSS upload credentials.

        The actual multipart upload is intentionally left to the caller so a
        future worker can stream large files without buffering them in memory.
        """
        data = await self.post("/nd.bizuserres.s/v1/get_res_center_token", {
            "capacity": 2,
            "name": name,
            "parentId": parent_id,
            "res": {"fileSize": size},
        })
        return data.get("data") or data

    async def wait_upload_file(self, task_id: str, timeout: float = 1800.0) -> str:
        deadline = asyncio.get_running_loop().time() + timeout
        while asyncio.get_running_loop().time() < deadline:
            data = await self.post("/nd.bizuserres.s/v1/file/get_info_by_task_id", {"taskId": task_id})
            payload = data.get("data") or {}
            file_id = str(payload.get("fileId") or "").strip()
            if file_id:
                return file_id
            await asyncio.sleep(1)
        raise GuangYaPanError(f"upload task timeout: {task_id}")

    @staticmethod
    def _upload_endpoint(value: str, bucket: str) -> str:
        endpoint = value.strip()
        if not endpoint.startswith(("http://", "https://")):
            endpoint = "https://" + endpoint
        # OpenList may return a bucket-qualified endpoint; oss2 expects the
        # service endpoint when the bucket is passed separately.
        prefix = bucket.strip() + "."
        if endpoint.split("//", 1)[-1].startswith(prefix):
            endpoint = endpoint.replace(prefix, "", 1)
        return endpoint

    async def upload_url(self, source_url: str, parent_id: str = "", name: str | None = None) -> SavedFile:
        """Download a source URL to a temporary file and upload it to GuangYaPan."""
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=15.0), follow_redirects=True) as source:
            async with source.stream("GET", source_url) as response:
                if response.status_code >= 400:
                    raise GuangYaPanError(f"source download status={response.status_code}")
                content_length = response.headers.get("content-length")
                size = int(content_length) if content_length and content_length.isdigit() else 0
                file_name = self._source_file_name(source_url)
                with tempfile.NamedTemporaryFile(prefix="guangyapan-", suffix=".upload", delete=False) as temp:
                    temp_path = temp.name
                    async for chunk in response.aiter_bytes(1024 * 1024):
                        temp.write(chunk)
                        size += 0 if content_length else len(chunk)
        try:
            session = await self.upload_session(parent_id, file_name, size)
            task_id = str(session.get("taskId") or "").strip()
            if not task_id:
                raise GuangYaPanError("upload session returned no task id")
            access_key = session.get("accessKeyID") or (session.get("creds") or {}).get("accessKeyID")
            secret_key = session.get("secretAccessKey") or (session.get("creds") or {}).get("secretAccessKey")
            security_token = session.get("sessionToken") or (session.get("creds") or {}).get("sessionToken")
            endpoint = session.get("endPoint") or session.get("fullEndPoint")
            bucket_name = session.get("bucketName")
            object_path = session.get("objectPath")
            if not all((access_key, secret_key, endpoint, bucket_name, object_path)):
                raise GuangYaPanError("upload session credentials are incomplete")
            auth = oss2.StsAuth(access_key, secret_key, security_token)
            bucket = oss2.Bucket(auth, self._upload_endpoint(endpoint, bucket_name), bucket_name)
            await asyncio.to_thread(bucket.put_object_from_file, object_path, temp_path)
            file_id = await self.wait_upload_file(task_id)
            playable = await self.download_url(file_id)
            return SavedFile("guangyapan", file_id, playable["url"], "upload", file_name, size)
        finally:
            try:
                os.unlink(temp_path)
            except OSError:
                pass

    async def save_url(self, source_url: str, mode: SaveMode, parent_id: str = "", name: str | None = None) -> SavedFile:
        if mode == "upload":
            return await self.upload_url(source_url, parent_id, name)
        if mode != "offline":
            raise GuangYaPanError(f"unsupported save mode: {mode}")
        task = await self.create_offline_task(source_url, parent_id, name)
        task_id = str(task.get("taskId") or "").strip()
        if not task_id:
            raise GuangYaPanError("offline task returned no task id")
        completed = await self.wait_offline_file(task_id)
        file_id = str(completed.get("fileId") or "").strip()
        playable = await self.download_url(file_id)
        return SavedFile("guangyapan", file_id, playable["url"], "offline", completed.get("fileName"), completed.get("totalSize"))

    @staticmethod
    def _source_file_name(source_url: str) -> str:
        """Use a stable URL digest so repeated saves cannot rename the file."""
        return hashlib.sha256(source_url.encode("utf-8")).hexdigest()
