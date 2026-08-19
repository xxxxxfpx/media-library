"""Compare one batch request with many single-item HTTP requests.

Run with the backend already started, for example:
    backend\\.venv\\Scripts\\python.exe backend\\scripts\\tools\\benchmark_batch_vs_single.py
"""

import argparse
import json
import statistics
import time
import uuid
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def post_json(url: str, payload: dict, token: str) -> tuple[float, dict]:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urlopen(request, timeout=60) as response:
            result = json.loads(response.read())
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    return time.perf_counter() - started, result


def login(base_url: str, username: str, password: str) -> str:
    _, result = post_json(
        f"{base_url}/api/user/login",
        {"username": username, "password": password},
        token="",
    )
    return result["access_token"]


def make_batch(prefix: str, tag_count: int) -> dict:
    movie_id = f"{prefix}-movie"
    items = [
        {
            "temp_id": movie_id,
            "source_info": {"source_id": f"{prefix}-movie"},
            "attrs": {"type": "Movie", "name": f"{prefix} movie"},
        }
    ]
    links = []
    for index in range(tag_count):
        tag_id = f"{prefix}-tag-{index}"
        items.append(
            {
                "temp_id": tag_id,
                "source_info": {},
                "attrs": {"type": "Tag", "name": f"{prefix} tag {index}"},
            }
        )
        links.append({"link": movie_id, "linked": tag_id})
    return {"source_name": prefix, "items": items, "item_links": links}


def run_once(base_url: str, token: str, tag_count: int) -> tuple[float, float, int]:
    prefix = f"bench-{uuid.uuid4().hex}"
    batch = make_batch(prefix, tag_count)

    batch_time, _ = post_json(f"{base_url}/api/media/batch", batch, token)

    single_started = time.perf_counter()
    movie_id = f"{prefix}-movie"
    for item in batch["items"]:
        single_payload = {
            "source_name": prefix,
            "items": [item],
            "item_links": [],
        }
        post_json(f"{base_url}/api/media/batch?strict_graph=false", single_payload, token)
    # The current API requires source_name and at least one item to resolve
    # temp_ids, so submit each link together with its two referenced items.
    item_by_id = {item["temp_id"]: item for item in batch["items"]}
    for link in batch["item_links"]:
        post_json(
            f"{base_url}/api/media/batch?strict_graph=false",
            {
                "source_name": prefix,
                "items": [item_by_id[link["link"]], item_by_id[link["linked"]]],
                "item_links": [link],
            },
            token,
        )
    single_time = time.perf_counter() - single_started
    return batch_time, single_time, 1 + tag_count + tag_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--token")
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="admin123")
    parser.add_argument("--tags", type=int, default=20)
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    token = args.token or login(base_url, args.username, args.password)
    results = [run_once(base_url, token, args.tags) for _ in range(args.rounds)]
    batch_times = [result[0] for result in results]
    single_times = [result[1] for result in results]
    requests = results[0][2]
    print(f"tags={args.tags}, rounds={args.rounds}, single_requests={requests}")
    print(f"batch_avg={statistics.mean(batch_times):.4f}s")
    print(f"single_avg={statistics.mean(single_times):.4f}s")
    print(f"ratio={statistics.mean(single_times) / statistics.mean(batch_times):.2f}x")
    for index, (batch_time, single_time, _) in enumerate(results, 1):
        print(f"round_{index}: batch={batch_time:.4f}s single={single_time:.4f}s")


if __name__ == "__main__":
    main()
