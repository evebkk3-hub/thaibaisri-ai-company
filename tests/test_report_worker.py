import os
import tempfile
import unittest
from pathlib import Path

from database.json_store import JsonStore
from reports.emailer import EmailConfig, SmtpEmailer
from workers.daily_executive_report import CompanyConfig, DailyExecutiveReportWorker


class ReportWorkerTest(unittest.TestCase):
    def test_generates_report_and_memory_without_smtp(self):
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)
                worker = DailyExecutiveReportWorker(
                    config=CompanyConfig(
                        channel_name="Thai Baisri",
                        current_subscribers=72200,
                        target_subscribers=100000,
                        youtube_api_key=None,
                        youtube_channel_id=None,
                    ),
                    store=JsonStore(Path("database")),
                    emailer=SmtpEmailer(EmailConfig(None, 587, None, None, None, None)),
                )
                path = worker.run()
                self.assertTrue(path.exists())
                report = path.read_text(encoding="utf-8")
                self.assertIn("Executive Report", report)
                self.assertTrue(Path("database/history.json").exists())

                second_path = worker.run()
                self.assertEqual(path, second_path)
                history = JsonStore(Path("database")).read("history.json", {})
                self.assertEqual(1, len(history["reports"]))
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
