"""Markdown report templates."""

from __future__ import annotations


def render_executive_report(channel_name: str, date_text: str, context: dict, results: dict) -> str:
    topic = context["recommended_topic"]
    goal = context["goal"]
    seo = results["seo"].data
    creative = results["creative"].data
    thumbnail = results["thumbnail"].data
    analytics = results["analytics"].data
    ceo = results["ceo"].data

    return f"""# Executive Report - {channel_name}

Date: {date_text}

## Today's Goal

Reach the next subscriber milestone through one focused, search-led video.

## Progress to 100K Subscribers

- Current subscribers: {goal["current_subscribers"]:,}
- Target subscribers: {goal["target_subscribers"]:,}
- Next company goal: {goal["next_goal"]:,}
- Progress: {analytics["subscriber_progress_percent"]:.2f}%

## Trend Analysis

- Seasonality: {results["trend"].data["seasonality"]}
- Signals: {", ".join(context["trend_signals"])}

## Recommended Topic

{topic["topic"]}

Reason: {topic["reason"]}

## SEO Keywords

{bullet_list(seo["keywords"])}

Hashtags: {" ".join(seo["hashtags"])}

## Titles

{numbered_list(creative["titles"])}

## Thumbnail

- Concept A: {thumbnail["concept_a"]}
- Concept B: {thumbnail["concept_b"]}
- CEO pick: {thumbnail["recommended"]}

## Hook

{bullet_list(creative["hooks"])}

## Outline

{numbered_list(creative["outline"])}

## Shorts Ideas

{bullet_list(creative["shorts"])}

## Community Post

{creative["community_post"]}

## KPI

- CTR target: {analytics["kpi"]["ctr_target"]}
- Shorts per video: {analytics["kpi"]["shorts_per_video"]}
- Daily subscriber target: {analytics["kpi"]["daily_subscriber_target"]}
- YouTube API status: {analytics["youtube_metrics"].get("status", "unknown")}

## CEO Decision

{ceo["decision"]}

## Daily Action Plan

1. Produce the recommended video.
2. Publish at least three Shorts from the same concept.
3. Post one Community update.
4. Pin a comment asking viewers what tutorial they want next.
5. Record views, CTR, retention, and subscriber gain for tomorrow's memory.
"""


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered_list(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))
