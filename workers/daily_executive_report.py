"""Daily executive report worker."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from agents import build_company_agents
from agents.base import AgentResult
from database.json_store import JsonStore
from integrations.google_trends import GoogleTrendsClient
from integrations.youtube import YouTubeDataClient
from memory.history import HistoryMemory
from reports.emailer import EmailConfig, SmtpEmailer
from reports.templates import render_executive_report


BKK = timezone(timedelta(hours=7))


TOPICS = [
    {
        "topic": "พานไหว้ครูบายศรีแบบง่าย ใช้ได้จริง สำหรับนักเรียน นักศึกษา และมือใหม่",
        "keywords": ["พานไหว้ครู", "บายศรี", "วิธีทำพาน", "ไหว้ครู", "งานฝีมือไทย"],
        "reason": "ตรงฤดูกาลเปิดเทอม/ไหว้ครู และตรงจุดแข็งของช่องด้านบายศรี",
        "score": 97,
    },
    {
        "topic": "บายศรีสู่ขวัญแบบประหยัด ทำเองได้ งบไม่สูง แต่ดูสวย",
        "keywords": ["บายศรีสู่ขวัญ", "บายศรีประหยัด", "ทำบายศรี", "พิธีไทย"],
        "reason": "เหมาะกับคนจัดงานเองและคนค้นหาวิธีลดงบ",
        "score": 94,
    },
    {
        "topic": "5 จุดที่มือใหม่ทำบายศรีพลาดบ่อย และวิธีแก้ให้สวยขึ้นทันที",
        "keywords": ["ทำบายศรี", "มือใหม่", "งานใบตอง", "แก้ปัญหา"],
        "reason": "คอนเทนต์แก้ปัญหามี retention สูง",
        "score": 93,
    },
    {
        "topic": "ทำพานบายศรีให้ดูแพง ด้วยเทคนิคจัดชั้นและเลือกสี",
        "keywords": ["พานบายศรี", "เทคนิค", "จัดพาน", "งานพิธี"],
        "reason": "คำว่า ดูแพง เพิ่มแรงจูงใจในการคลิก",
        "score": 91,
    },
    {
        "topic": "ASMR พับใบตอง ทำบายศรี เสียงธรรมชาติ ผ่อนคลาย",
        "keywords": ["ASMR", "พับใบตอง", "บายศรี", "ผ่อนคลาย", "งานฝีมือ"],
        "reason": "เป็นมุมใหม่ที่เหมาะกับ Shorts/Reels",
        "score": 89,
    },
]


@dataclass
class CompanyConfig:
    channel_name: str
    current_subscribers: int
    target_subscribers: int
    youtube_api_key: str | None
    youtube_channel_id: str | None

    @property
    def next_goal(self) -> int:
        if self.current_subscribers < 100_000:
            return 100_000
        if self.current_subscribers < 500_000:
            return 500_000
        return 1_000_000


class DailyExecutiveReportWorker:
    """Coordinates agents, memory, database, reports, and email delivery."""

    def __init__(self, config: CompanyConfig, store: JsonStore, emailer: SmtpEmailer) -> None:
        self.config = config
        self.store = store
        self.memory = HistoryMemory(store)
        self.emailer = emailer
        self.agents = build_company_agents()
        self.youtube = YouTubeDataClient(config.youtube_api_key, config.youtube_channel_id)
        self.trends = GoogleTrendsClient()

    @classmethod
    def from_environment(cls) -> "DailyExecutiveReportWorker":
        config = CompanyConfig(
            channel_name=os.getenv("CHANNEL_NAME", "Thai Baisri"),
            current_subscribers=int(os.getenv("CURRENT_SUBSCRIBERS", "72200")),
            target_subscribers=int(os.getenv("TARGET_SUBSCRIBERS", "100000")),
            youtube_api_key=os.getenv("YOUTUBE_API_KEY") or None,
            youtube_channel_id=os.getenv("YOUTUBE_CHANNEL_ID") or None,
        )
        return cls(
            config=config,
            store=JsonStore(Path("database")),
            emailer=SmtpEmailer(EmailConfig.from_environment()),
        )

    def run(self) -> Path:
        today = datetime.now(BKK).strftime("%Y-%m-%d")
        history = self.memory.load()
        context = {
            "topics": TOPICS,
            "history": history,
            "goal": {
                "current_subscribers": self.config.current_subscribers,
                "target_subscribers": self.config.target_subscribers,
                "next_goal": self.config.next_goal,
            },
            "trend_signals": self._trend_signals(),
            "youtube_metrics": self._youtube_metrics(),
        }

        existing_topic = self.memory.topic_for_date(today)
        if existing_topic:
            selected_topic = next(
                (topic for topic in TOPICS if topic["topic"] == existing_topic),
                TOPICS[0],
            )
            fallback_research = self.agents["research"].run({**context, "history": {"used_topics": []}})
            research = AgentResult(
                agent=fallback_research.agent,
                summary=f"Reused existing topic for {today}: {selected_topic['topic']}",
                data={**fallback_research.data, "topic": selected_topic},
            )
        else:
            research = self.agents["research"].run(context)
        context["recommended_topic"] = research.data["topic"]
        results = {
            "research": research,
            "trend": self.agents["trend"].run(context),
            "seo": self.agents["seo"].run(context),
            "creative": self.agents["creative"].run(context),
            "thumbnail": self.agents["thumbnail"].run(context),
            "analytics": self.agents["analytics"].run(context),
        }
        results["ceo"] = self.agents["ceo"].run(context)

        report = render_executive_report(
            channel_name=self.config.channel_name,
            date_text=today,
            context=context,
            results=results,
        )
        report_path = Path("reports/daily-reports") / f"executive-report-{today}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")

        self.memory.remember_topic(context["recommended_topic"]["topic"], today)
        self.store.write(
            "latest_kpi.json",
            {
                "date": today,
                "channel_name": self.config.channel_name,
                "current_subscribers": self.config.current_subscribers,
                "target_subscribers": self.config.target_subscribers,
                "recommended_topic": context["recommended_topic"]["topic"],
                "youtube_metrics": context["youtube_metrics"],
            },
        )
        self.emailer.send(subject=f"Thai Baisri Executive Report - {today}", body=report)
        return report_path

    def _trend_signals(self) -> list[str]:
        return self.trends.daily_signals()

    def _youtube_metrics(self) -> dict:
        return self.youtube.channel_statistics()
