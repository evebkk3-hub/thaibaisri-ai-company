"""Content history memory."""

from __future__ import annotations

from database.json_store import JsonStore


class HistoryMemory:
    """Prevents duplicate content and stores daily learning."""

    FILE_NAME = "history.json"

    def __init__(self, store: JsonStore) -> None:
        self.store = store

    def load(self) -> dict:
        return self.store.read(self.FILE_NAME, {"used_topics": [], "reports": []})

    def topic_for_date(self, date_text: str) -> str | None:
        history = self.load()
        for report in history.get("reports", []):
            if report.get("date") == date_text:
                return report.get("topic")
        return None

    def remember_topic(self, topic: str, date_text: str) -> None:
        history = self.load()
        history.setdefault("used_topics", [])
        if topic not in history["used_topics"]:
            history["used_topics"].append(topic)
        reports = history.setdefault("reports", [])
        for report in reports:
            if report.get("date") == date_text:
                report["topic"] = topic
                break
        else:
            reports.append({"date": date_text, "topic": topic})
        self.store.write(self.FILE_NAME, history)
