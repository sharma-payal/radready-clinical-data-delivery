from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryPolicyTest(unittest.TestCase):
    def test_no_source_or_bulk_delivery_data_is_tracked(self) -> None:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        tracked = set(result.stdout.splitlines())
        self.assertFalse(any(path.startswith("data/raw/") for path in tracked))
        allowed_artifact = "artifacts/delivery/dashboard.html"
        self.assertFalse(any(path.startswith("artifacts/delivery/") and path != allowed_artifact for path in tracked))

    def test_license_and_privacy_documents_are_present(self) -> None:
        for path in ("LICENSE", "DATA_LICENSE.md", "PRIVACY.md", "SECURITY.md"):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_rights_registry_contains_no_external_dataset(self) -> None:
        registry = json.loads((ROOT / "config" / "data_rights_registry.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["project_mode"], "synthetic_only")
        self.assertEqual(registry["external_datasets"], [])
        self.assertEqual(registry["generated_data_license"], "CC0-1.0")
        self.assertTrue(all(provider["is_fictional"] for provider in registry["providers"]))


if __name__ == "__main__":
    unittest.main()
