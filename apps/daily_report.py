"""Daily executive report command."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from workers.daily_executive_report import DailyExecutiveReportWorker


def main() -> None:
    worker = DailyExecutiveReportWorker.from_environment()
    worker.run()


if __name__ == "__main__":
    main()
