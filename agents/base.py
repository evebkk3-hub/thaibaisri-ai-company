"""Base contracts shared by AI company agents."""

from __future__ import annotations

from dataclasses import dataclass
@dataclass(frozen=True)
class AgentResult:
    """Structured result returned by every agent."""

    agent: str
    summary: str
    data: dict
