from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from radready.pipeline import run_delivery
from radready.synthetic import generate_dataset


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "config" / "customer_spec.json"


class DeliveryPipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.raw = root / "raw"
        self.output = root / "delivery"
        generate_dataset(self.raw, seed=42, patient_count=180)
        self.report = run_delivery(self.raw, self.output, SPEC)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _rows(self, name: str) -> list[dict[str, str]]:
        with (self.output / name).open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def test_seeded_defects_are_quarantined(self) -> None:
        reasons = "|".join(row["reasons"] for row in self._rows("quarantine_log.csv"))
        self.assertIn("missing_required_metadata", reasons)
        self.assertIn("duplicate_study_uid", reasons)
        self.assertIn("missing_report", reasons)
        self.assertIn("phi_pattern_detected", reasons)
        self.assertEqual(self.report["delivery_counts"]["orphan_reports"], 1)

    def test_delivery_obeys_contract(self) -> None:
        spec = json.loads(SPEC.read_text(encoding="utf-8"))
        patients = {row["patient_token"]: row for row in self._rows("patients.csv")}
        studies = self._rows("studies.csv")
        reports = {row["study_uid"]: row for row in self._rows("reports.csv")}
        counts: dict[str, int] = {}
        dates: dict[str, list[str]] = {}
        for study in studies:
            counts[study["patient_token"]] = counts.get(study["patient_token"], 0) + 1
            dates.setdefault(study["patient_token"], []).append(study["study_date"])
            self.assertEqual(study["modality"], spec["cohort"]["modality"])
            self.assertEqual(study["body_part"], spec["cohort"]["body_part"])
            self.assertEqual(study["license_status"], "approved")
            self.assertEqual(reports[study["study_uid"]]["signed_status"], "final")
            self.assertEqual(patients[study["patient_token"]]["consent"], "research")
            self.assertGreaterEqual(int(patients[study["patient_token"]]["age"]), 18)
        self.assertTrue(counts)
        self.assertTrue(all(value >= 2 for value in counts.values()))
        from datetime import date
        for patient_dates in dates.values():
            parsed = sorted(date.fromisoformat(value) for value in patient_dates)
            interval = (parsed[-1] - parsed[0]).days
            self.assertGreaterEqual(interval, spec["cohort"]["minimum_followup_days"])
            self.assertLessEqual(interval, spec["cohort"]["maximum_followup_days"])

    def test_manifest_hashes_match_delivered_rows(self) -> None:
        studies = {row["study_uid"]: row for row in self._rows("studies.csv")}
        manifest = self._rows("cohort_manifest.csv")
        self.assertEqual(len(manifest), len(studies))
        for item in manifest:
            canonical = json.dumps(studies[item["study_uid"]], sort_keys=True, separators=(",", ":"))
            expected = hashlib.sha256(canonical.encode()).hexdigest()
            self.assertEqual(item["record_sha256"], expected)

    def test_all_contractual_quality_gates_pass(self) -> None:
        self.assertEqual(self.report["delivery_status"], "READY")
        self.assertTrue(all(gate["status"] == "PASS" for gate in self.report["quality_gates"].values()))

    def test_generation_is_deterministic(self) -> None:
        second_raw = Path(self.temp.name) / "raw_second"
        generate_dataset(second_raw, seed=42, patient_count=180)
        for name in ("patients.csv", "studies.csv", "reports.csv"):
            self.assertEqual((self.raw / name).read_bytes(), (second_raw / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
