"""SMTP email delivery with graceful retries."""

from __future__ import annotations

import os
import smtplib
import time
from dataclasses import dataclass
from email.mime.text import MIMEText


@dataclass
class EmailConfig:
    host: str | None
    port: int
    username: str | None
    password: str | None
    mail_from: str | None
    mail_to: str | None
    retries: int = 3

    @classmethod
    def from_environment(cls) -> "EmailConfig":
        return cls(
            host=os.getenv("SMTP_HOST") or None,
            port=int(os.getenv("SMTP_PORT", "587") or "587"),
            username=os.getenv("SMTP_USER") or None,
            password=os.getenv("SMTP_PASSWORD") or None,
            mail_from=os.getenv("MAIL_FROM") or os.getenv("SMTP_USER") or None,
            mail_to=os.getenv("MAIL_TO") or None,
        )

    def is_configured(self) -> bool:
        return all([self.host, self.username, self.password, self.mail_from, self.mail_to])


class SmtpEmailer:
    """Send email without failing the whole company if SMTP is missing."""

    def __init__(self, config: EmailConfig) -> None:
        self.config = config

    def send(self, subject: str, body: str) -> bool:
        if not self.config.is_configured():
            print("SMTP is not fully configured; report generated without email.")
            return False

        message = MIMEText(body, "plain", "utf-8")
        message["Subject"] = subject
        message["From"] = self.config.mail_from
        message["To"] = self.config.mail_to

        last_error: Exception | None = None
        for attempt in range(1, self.config.retries + 1):
            try:
                with smtplib.SMTP(self.config.host, self.config.port, timeout=30) as server:
                    server.starttls()
                    server.login(self.config.username, self.config.password)
                    server.send_message(message)
                return True
            except Exception as exc:
                last_error = exc
                time.sleep(min(attempt * 2, 10))

        print(f"SMTP delivery failed after {self.config.retries} attempts: {last_error}")
        return False
