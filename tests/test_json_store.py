import tempfile
import unittest
from pathlib import Path

from database.json_store import JsonStore


class JsonStoreTest(unittest.TestCase):
    def test_read_default_and_write_roundtrip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = JsonStore(Path(temp_dir))
            self.assertEqual({"ok": True}, store.read("missing.json", {"ok": True}))
            store.write("sample.json", {"topic": "บายศรี"})
            self.assertEqual({"topic": "บายศรี"}, store.read("sample.json", {}))


if __name__ == "__main__":
    unittest.main()
