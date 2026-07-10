import unittest

from integrations.google_trends import GoogleTrendsClient
from integrations.youtube import YouTubeDataClient


class IntegrationBoundaryTest(unittest.TestCase):
    def test_google_trends_fallback_signals(self):
        self.assertIn("บายศรี", GoogleTrendsClient().daily_signals())

    def test_youtube_client_missing_config_is_safe(self):
        self.assertEqual({"status": "not_configured"}, YouTubeDataClient(None, None).channel_statistics())


if __name__ == "__main__":
    unittest.main()
