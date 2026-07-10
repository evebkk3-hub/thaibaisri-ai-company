"""Production agent implementations.

The agents are deterministic by default so scheduled GitHub Actions can run
without paid AI dependencies. External AI providers can be added behind these
interfaces later without changing the worker.
"""

from __future__ import annotations

from dataclasses import dataclass

from agents.base import AgentResult


@dataclass
class SimpleAgent:
    name: str
    role: str

    def run(self, context: dict) -> AgentResult:
        return AgentResult(agent=self.name, summary=self.role, data={})


class CEOAgent(SimpleAgent):
    def __init__(self) -> None:
        super().__init__("CEO Agent", "Owns final decision, priority, and KPI discipline.")

    def run(self, context: dict) -> AgentResult:
        goal = context["goal"]
        topic = context["recommended_topic"]
        remaining = max(0, goal["target_subscribers"] - goal["current_subscribers"])
        decision = (
            f"Produce and market one focused video about '{topic['topic']}'. "
            "Do not split the team across multiple topics today."
        )
        return AgentResult(
            agent=self.name,
            summary=decision,
            data={
                "decision": decision,
                "remaining_subscribers": remaining,
                "next_goal": goal["next_goal"],
            },
        )


class ResearchAgent(SimpleAgent):
    def __init__(self) -> None:
        super().__init__("Research Agent", "Finds practical audience problems.")

    def run(self, context: dict) -> AgentResult:
        used = set(context["history"].get("used_topics", []))
        candidates = [topic for topic in context["topics"] if topic["topic"] not in used]
        if not candidates:
            candidates = context["topics"]
        ranked = sorted(candidates, key=lambda item: item["score"], reverse=True)
        return AgentResult(
            agent=self.name,
            summary=f"Selected {ranked[0]['topic']} from {len(ranked)} candidates.",
            data={"topic": ranked[0], "alternates": ranked[1:4]},
        )


class TrendAgent(SimpleAgent):
    def __init__(self) -> None:
        super().__init__("Trend Agent", "Combines trend fallback signals with seasonal context.")

    def run(self, context: dict) -> AgentResult:
        topic = context["recommended_topic"]
        seasonality = "ไหว้ครู/เปิดเทอม" if "ไหว้ครู" in topic["topic"] else "งานพิธีไทย"
        return AgentResult(
            agent=self.name,
            summary=f"Trend angle: {seasonality}.",
            data={"seasonality": seasonality, "google_trends": context.get("trend_signals", [])},
        )


class SEOAgent(SimpleAgent):
    def __init__(self) -> None:
        super().__init__("SEO Agent", "Builds keywords, hashtags, and search positioning.")

    def run(self, context: dict) -> AgentResult:
        topic = context["recommended_topic"]
        keywords = list(dict.fromkeys(topic["keywords"] + ["Thai Baisri", "งานฝีมือไทย"]))
        hashtags = ["#ThaiBaisri", "#บายศรี", "#งานฝีมือไทย", "#DIYThaiCraft"]
        return AgentResult(
            agent=self.name,
            summary="SEO package generated.",
            data={"keywords": keywords, "hashtags": hashtags},
        )


class CreativeAgent(SimpleAgent):
    def __init__(self) -> None:
        super().__init__("Creative Agent", "Creates titles, hooks, outlines, and posts.")

    def run(self, context: dict) -> AgentResult:
        topic = context["recommended_topic"]["topic"]
        titles = [
            f"{topic} | สอนละเอียดทีละขั้นตอน",
            f"มือใหม่ต้องดู! {topic}",
            f"ทำเองได้จริง: {topic}",
            f"{topic} แบบง่าย สวย และประหยัด",
            f"เทคนิคจาก Thai Baisri: {topic}",
            f"เริ่มทำบายศรีจากศูนย์ด้วยหัวข้อนี้",
            f"อย่าเพิ่งทำบายศรี ถ้ายังไม่รู้วิธีนี้",
            f"ทำให้งานพิธีดูสวยขึ้นด้วย {topic}",
            f"คลิปเดียวเข้าใจ {topic}",
            f"{topic} สำหรับคนมีเวลาน้อย",
        ]
        hooks = [
            "ถ้าคุณเป็นมือใหม่ คลิปนี้จะพาทำแบบไม่ข้ามขั้นตอน",
            "หลายคนพลาดตรงนี้เวลาเริ่มทำบายศรี วันนี้เราจะแก้ให้เห็นชัด",
            "เริ่มจากวัสดุธรรมดา แล้วทำให้กลายเป็นงานพิธีที่ใช้ได้จริง",
        ]
        outline = [
            "เปิดด้วยภาพผลงานสำเร็จ",
            "บอกปัญหาของมือใหม่",
            "แนะนำวัสดุทั้งหมด",
            "สอนขั้นตอนหลักทีละขั้น",
            "แทรกเทคนิคให้งานแน่นและสวย",
            "สรุปก่อน-หลัง",
            "ชวนคอมเมนต์หัวข้อถัดไป",
        ]
        shorts = ["Before/After", "3 เทคนิคเร็ว", "ข้อผิดพลาดมือใหม่", "Checklist วัสดุ", "Final reveal"]
        community_post = (
            "ใครกำลังเตรียมงานพิธีหรืองานไหว้ครู คลิปวันนี้ทำตามได้จริง "
            "คอมเมนต์ปัญหาที่ติดอยู่ไว้ได้เลยค่ะ"
        )
        return AgentResult(
            agent=self.name,
            summary="Creative package generated.",
            data={
                "titles": titles,
                "hooks": hooks,
                "outline": outline,
                "shorts": shorts,
                "community_post": community_post,
            },
        )


class ThumbnailAgent(SimpleAgent):
    def __init__(self) -> None:
        super().__init__("Thumbnail Agent", "Designs thumbnail concepts and A/B tests.")

    def run(self, context: dict) -> AgentResult:
        return AgentResult(
            agent=self.name,
            summary="Thumbnail A/B concepts generated.",
            data={
                "concept_a": "Before/After: วัสดุธรรมดา -> ผลงานสำเร็จ | Text: มือใหม่ก็ทำได้",
                "concept_b": "ผลงานสำเร็จเต็มจอ | Text: สวย ใช้ได้จริง",
                "recommended": "concept_a",
            },
        )


class AnalyticsAgent(SimpleAgent):
    def __init__(self) -> None:
        super().__init__("Analytics Agent", "Tracks KPI and learning loops.")

    def run(self, context: dict) -> AgentResult:
        youtube = context.get("youtube_metrics", {})
        goal = context["goal"]
        progress = round(goal["current_subscribers"] / goal["target_subscribers"] * 100, 2)
        return AgentResult(
            agent=self.name,
            summary=f"Subscriber progress is {progress}%.",
            data={
                "subscriber_progress_percent": progress,
                "youtube_metrics": youtube,
                "kpi": {
                    "ctr_target": ">= 5%",
                    "shorts_per_video": 3,
                    "daily_subscriber_target": max(
                        1, round((goal["target_subscribers"] - goal["current_subscribers"]) / 90)
                    ),
                },
            },
        )


def build_company_agents() -> dict[str, SimpleAgent]:
    """Return all agents requested by the operating model."""

    return {
        "ceo": CEOAgent(),
        "hr": SimpleAgent("HR Agent", "Reviews team workload and accountability."),
        "research": ResearchAgent(),
        "trend": TrendAgent(),
        "seo": SEOAgent(),
        "creative": CreativeAgent(),
        "script": SimpleAgent("Script Agent", "Expands outlines into production scripts."),
        "thumbnail": ThumbnailAgent(),
        "analytics": AnalyticsAgent(),
        "marketing": SimpleAgent("Marketing Agent", "Prepares distribution actions."),
        "qa": SimpleAgent("QA Agent", "Checks quality and duplication risk."),
        "innovation": SimpleAgent("Innovation Agent", "Suggests repeatable content formats."),
        "database": SimpleAgent("Database Agent", "Protects JSON storage and migration boundaries."),
        "memory": SimpleAgent("Memory Agent", "Stores learning and prevents duplicate topics."),
        "scheduler": SimpleAgent("Scheduler Agent", "Owns automation reliability."),
    }
