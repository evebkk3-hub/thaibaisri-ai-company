"""YouTube Data API adapter."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request


class YouTubeDataClient:
    """Small YouTube Data API client using only the Python standard library."""

    BASE_URL = "https://www.googleapis.com/youtube/v3/channels"

    def __init__(self, api_key: str | None, channel_id: str | None) -> None:
        self.api_key = api_key
        self.channel_id = channel_id

    def is_configured(self) -> bool:
        return bool(self.api_key and self.channel_id)

    def channel_statistics(self) -> dict:
        if not self.is_configured():
            return {"status": "not_configured"}

        params = urllib.parse.urlencode(
            {
                "part": "statistics,snippet",
                "id": self.channel_id,
                "key": self.api_key,
            }
        )
        url = f"{self.BASE_URL}?{params}"
        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

        items = payload.get("items", [])
        if not items:
            return {"status": "not_found"}

        item = items[0]
        return {
            "status": "ok",
            "title": item.get("snippet", {}).get("title"),
            "statistics": item.get("statistics", {}),
        }
