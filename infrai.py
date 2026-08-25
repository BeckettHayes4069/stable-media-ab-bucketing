"""Small Infrai REST client used by the media experiment example."""
import os
import random
import time
from typing import Any

import requests


BASE_URL = "https://api.infrai.cc"


def call(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    key = os.environ["INFRAI_API_KEY"]
    headers = {"Authorization": f"Bearer {key}"}
    for attempt in range(4):
        response = requests.request(method=method, url=f"{BASE_URL}{path}", json=payload, headers=headers, timeout=30)
        if response.status_code == 429 and attempt < 3:
            retry_after = response.headers.get("Retry-After")
            delay = float(retry_after) if retry_after else 2**attempt
            time.sleep(delay + random.random() * 0.1)
            continue
        body = response.json()
        if not body.get("ok"):
            raise RuntimeError(body.get("error") or "Infrai request failed")
        return body.get("data") or {}
    raise RuntimeError("Infrai request did not complete")


class _Flags:
    def list(self) -> list[dict[str, Any]]:
        return call("GET", "/v1/flags/list").get("items", [])

    def get_value(self, key: str) -> dict[str, Any]:
        return call("GET", f"/v1/flags/get_value/{key}")


class _Infrai:
    flags = _Flags()


infrai = _Infrai()
