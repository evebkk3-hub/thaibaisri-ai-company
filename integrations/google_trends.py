"""Google Trends integration boundary.

Google does not provide a simple official public Trends API. This adapter keeps
the worker independent from any specific unofficial client. A future
implementation can add pytrends or a paid trends provider behind this class.
"""

from __future__ import annotations


class GoogleTrendsClient:
    """Return trend signals without making the report depend on an external package."""

    def __init__(self, fallback_keywords: list[str] | None = None) -> None:
        self.fallback_keywords = fallback_keywords or ["ไหว้ครู", "บายศรี", "งานฝีมือไทย", "DIY"]

    def daily_signals(self) -> list[str]:
        return self.fallback_keywords
