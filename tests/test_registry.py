"""
Unit tests for DeveloperOS Tool Registry integrity.
Runs with standard unittest module.
"""

import sys
import unittest
from pathlib import Path

# Ensure registry directory is in sys.path
REGISTRY_ROOT = Path(__file__).resolve().parent.parent
if str(REGISTRY_ROOT) not in sys.path:
    sys.path.insert(0, str(REGISTRY_ROOT))

from registry_manager import RegistryManager


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.manager = RegistryManager()

    def test_registry_loads_successfully(self):
        self.assertIsNotNone(self.manager.version)
        self.assertGreater(len(self.manager.suites), 0)
        self.assertGreater(len(self.manager.tools), 0)

    def test_ten_suites_present(self):
        self.assertEqual(len(self.manager.suites), 10)

    def test_integrity_no_errors(self):
        errors = self.manager.validate_integrity()
        self.assertEqual(errors, [], f"Registry integrity errors: {errors}")

    def test_search_functionality(self):
        results = self.manager.search_tools("json")
        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()
