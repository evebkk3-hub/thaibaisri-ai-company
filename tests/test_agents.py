import unittest

from agents import build_company_agents


class AgentRegistryTest(unittest.TestCase):
    def test_all_required_agents_exist(self):
        agents = build_company_agents()
        expected = {
            "ceo",
            "hr",
            "research",
            "trend",
            "seo",
            "creative",
            "script",
            "thumbnail",
            "analytics",
            "marketing",
            "qa",
            "innovation",
            "database",
            "memory",
            "scheduler",
        }
        self.assertEqual(expected, set(agents))


if __name__ == "__main__":
    unittest.main()
