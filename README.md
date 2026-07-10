# ThaiBaisri AI Company

Production-oriented AI company automation for the Thai Baisri YouTube channel.

## Mission

Every morning, the company researches opportunities, selects one recommended
video, prepares SEO and creative assets, tracks KPI, stores memory, and emails
an executive report.

## Architecture

```text
apps/                 Python entrypoints
workers/              Scheduled business workflows
agents/               CEO, research, trend, SEO, creative, analytics, and support agents
memory/               Learning and duplicate-prevention memory
database/             JSON database now, PostgreSQL boundary later
reports/              Markdown report templates and SMTP emailer
prompts/              Future LLM prompt templates
dashboard/            Future KPI dashboard
tests/                Unit tests
.github/workflows/    CI and daily 08:00 Asia/Bangkok automation
```

## Daily Automation

GitHub Actions runs `Daily Executive Report` every day at:

- `08:00 Asia/Bangkok`
- `01:00 UTC`

The workflow:

1. Checks out the repository.
2. Sets up Python 3.11.
3. Runs unit tests.
4. Generates the daily executive report.
5. Sends email if SMTP secrets are configured.
6. Commits report, memory, and KPI JSON updates.

## Required GitHub Secrets

```text
SMTP_HOST
SMTP_PORT
SMTP_USER
SMTP_PASSWORD
MAIL_FROM
MAIL_TO
```

Optional:

```text
YOUTUBE_API_KEY
YOUTUBE_CHANNEL_ID
```

## Local Run

```powershell
python -m unittest discover -s tests -p "test_*.py" -t .
python apps/daily_report.py
```

Reports are written to:

```text
reports/daily-reports/
```

Memory and KPI snapshots are stored in:

```text
database/
```

## Quality Rules

- Never duplicate content recommendations when memory has alternatives.
- Never fail the full report because SMTP or YouTube API is missing.
- Store history for future learning.
- Keep external integrations behind adapters.
- Prefer deterministic defaults for reliable scheduled automation.
