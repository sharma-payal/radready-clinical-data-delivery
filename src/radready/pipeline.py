from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


PHI_PATTERNS = {
    "phone_number": re.compile(r"\b(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b"),
    "medical_record_number": re.compile(r"\b(?:MRN|medical record)\s*[:#]?\s*[A-Z0-9-]{5,}\b", re.I),
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0]) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _ratio(passed: int, total: int) -> float:
    return round(passed / total, 4) if total else 0.0


def _sha256_row(row: dict[str, str]) -> str:
    canonical = json.dumps(row, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def _scan_phi(text: str) -> list[str]:
    return [name for name, pattern in PHI_PATTERNS.items() if pattern.search(text)]


def run_delivery(raw_dir: Path, output_dir: Path, spec_path: Path) -> dict[str, Any]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    patients = read_csv(raw_dir / "patients.csv")
    studies = read_csv(raw_dir / "studies.csv")
    reports = read_csv(raw_dir / "reports.csv")
    patient_by_id = {row["patient_token"]: row for row in patients}
    report_by_study: dict[str, dict[str, str]] = {}
    report_counts = Counter(row["study_uid"] for row in reports)
    for report in reports:
        report_by_study.setdefault(report["study_uid"], report)

    uid_counts = Counter(row["study_uid"] for row in studies)
    required_fields = spec["required_study_fields"]
    quarantine: list[dict[str, str]] = []
    valid_studies: list[dict[str, str]] = []
    reason_counts: Counter[str] = Counter()

    complete_fields = 0
    total_fields = len(studies) * len(required_fields)
    for study in studies:
        complete_fields += sum(bool(study.get(field, "").strip()) for field in required_fields)
        reasons: list[str] = []
        missing = [field for field in required_fields if not study.get(field, "").strip()]
        if missing:
            reasons.append("missing_required_metadata")
        if uid_counts[study["study_uid"]] > 1:
            reasons.append("duplicate_study_uid")
        if study["patient_token"] not in patient_by_id:
            reasons.append("orphan_study")
        try:
            date.fromisoformat(study["study_date"])
        except ValueError:
            reasons.append("invalid_study_date")
        report = report_by_study.get(study["study_uid"])
        if not report:
            reasons.append("missing_report")
        else:
            phi_hits = _scan_phi(" ".join([report["report_text"], report["impression"]]))
            if phi_hits:
                reasons.append("phi_pattern_detected")
            if report_counts[study["study_uid"]] > 1:
                reasons.append("multiple_reports_per_study")
        if reasons:
            for reason in set(reasons):
                reason_counts[reason] += 1
            quarantine.append({
                "study_uid": study["study_uid"],
                "patient_token": study["patient_token"],
                "reasons": "|".join(sorted(set(reasons))),
                "disposition": "excluded_pending_remediation",
            })
        else:
            valid_studies.append(study)

    study_uids = set(uid_counts)
    orphan_reports = sum(report["study_uid"] not in study_uids for report in reports)
    if orphan_reports:
        reason_counts["orphan_report"] = orphan_reports

    cohort = spec["cohort"]
    candidate_by_patient: dict[str, list[dict[str, str]]] = defaultdict(list)
    exclusion_counts: Counter[str] = Counter()
    for study in valid_studies:
        patient = patient_by_id[study["patient_token"]]
        filters = {
            "wrong_modality": study["modality"] != cohort["modality"],
            "wrong_body_part": study["body_part"] != cohort["body_part"],
            "under_minimum_age": int(patient["age"]) < cohort["minimum_age"],
            "consent_not_eligible": cohort["require_research_consent"] and patient["consent"] != "research",
            "license_not_approved": study["license_status"] != cohort["required_license_status"],
            "report_not_final": cohort["require_signed_report"] and report_by_study[study["study_uid"]]["signed_status"] != "final",
        }
        failed = [name for name, did_fail in filters.items() if did_fail]
        if failed:
            exclusion_counts.update(failed)
        else:
            candidate_by_patient[study["patient_token"]].append(study)

    selected_studies: list[dict[str, str]] = []
    selected_patients: list[str] = []
    timeline_rows: list[dict[str, Any]] = []
    for patient_token, patient_studies in candidate_by_patient.items():
        ordered = sorted(patient_studies, key=lambda row: row["study_date"])
        if len(ordered) < cohort["minimum_studies_per_patient"]:
            exclusion_counts["insufficient_longitudinal_studies"] += 1
            continue
        followup_days = (date.fromisoformat(ordered[-1]["study_date"]) - date.fromisoformat(ordered[0]["study_date"])).days
        if followup_days < cohort["minimum_followup_days"]:
            exclusion_counts["followup_too_short"] += 1
            continue
        if followup_days > cohort["maximum_followup_days"]:
            exclusion_counts["followup_too_long"] += 1
            continue
        selected_patients.append(patient_token)
        selected_studies.extend(ordered)
        timeline_rows.append({
            "patient_token": patient_token,
            "studies": len(ordered),
            "first_study": ordered[0]["study_date"],
            "last_study": ordered[-1]["study_date"],
            "followup_days": followup_days,
        })

    selected_patient_set = set(selected_patients)
    selected_patient_rows = [row for row in patients if row["patient_token"] in selected_patient_set]
    selected_uids = {row["study_uid"] for row in selected_studies}
    selected_reports = [row for row in reports if row["study_uid"] in selected_uids]

    manifest = []
    for study in selected_studies:
        manifest.append({
            "project_id": spec["project_id"],
            "patient_token": study["patient_token"],
            "study_uid": study["study_uid"],
            "study_date": study["study_date"],
            "report_id": report_by_study[study["study_uid"]]["report_id"],
            "source_site": study["source_site"],
            "record_sha256": _sha256_row(study),
        })

    metadata_completeness = _ratio(complete_fields, total_fields)
    linked_reports = sum(bool(report_by_study.get(study["study_uid"])) for study in studies)
    report_linkage = _ratio(linked_reports, len(studies))
    reports_without_phi = sum(not _scan_phi(" ".join([r["report_text"], r["impression"]])) for r in reports)
    phi_scan_pass = _ratio(reports_without_phi, len(reports))
    longitudinal_coverage = 1.0 if selected_studies and all(t["studies"] >= cohort["minimum_studies_per_patient"] for t in timeline_rows) else 0.0
    license_approval = _ratio(sum(s["license_status"] == cohort["required_license_status"] for s in selected_studies), len(selected_studies))
    metrics = {
        "metadata_completeness": metadata_completeness,
        "report_linkage": report_linkage,
        "phi_scan_pass": phi_scan_pass,
        "longitudinal_coverage": longitudinal_coverage,
        "license_approval": license_approval,
    }
    weights = {
        "metadata_completeness": 0.25,
        "report_linkage": 0.20,
        "phi_scan_pass": 0.20,
        "longitudinal_coverage": 0.20,
        "license_approval": 0.15,
    }
    readiness_score = round(sum(metrics[key] * weight for key, weight in weights.items()) * 100, 2)
    threshold_map = {
        "metadata_completeness": "metadata_completeness_min",
        "report_linkage": "report_linkage_min",
        "phi_scan_pass": "phi_scan_pass_min",
        "longitudinal_coverage": "longitudinal_coverage_min",
        "license_approval": "license_approval_min",
    }
    gates = {
        key: {
            "actual": value,
            "threshold": spec["quality_gates"][threshold_map[key]],
            "status": "PASS" if value >= spec["quality_gates"][threshold_map[key]] else "FAIL",
        }
        for key, value in metrics.items()
    }

    report = {
        "project_id": spec["project_id"],
        "customer": spec["customer"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_classification": "SYNTHETIC — NOT FOR CLINICAL USE",
        "delivery_status": "READY" if all(g["status"] == "PASS" for g in gates.values()) else "REVIEW_REQUIRED",
        "readiness_score": readiness_score,
        "source_counts": {"patients": len(patients), "studies": len(studies), "reports": len(reports)},
        "delivery_counts": {
            "patients": len(selected_patients),
            "studies": len(selected_studies),
            "reports": len(selected_reports),
            "quarantined_studies": len(quarantine),
            "orphan_reports": orphan_reports,
        },
        "quality_gates": gates,
        "quarantine_reasons": dict(reason_counts.most_common()),
        "cohort_exclusions": dict(exclusion_counts.most_common()),
        "sample_timelines": sorted(timeline_rows, key=lambda row: row["followup_days"], reverse=True)[:8],
        "limitations": [
            "All records are synthetic and demonstrate operations, not clinical validity.",
            "Regex screening is a first-pass safeguard and does not replace expert de-identification certification.",
            "DICOM pixels are represented by metadata only; image-level QC is outside this demo scope.",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "patients.csv", selected_patient_rows)
    write_csv(output_dir / "studies.csv", selected_studies)
    write_csv(output_dir / "reports.csv", selected_reports)
    write_csv(output_dir / "cohort_manifest.csv", manifest)
    write_csv(output_dir / "quarantine_log.csv", quarantine, ["study_uid", "patient_token", "reasons", "disposition"])
    (output_dir / "qc_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    _write_acceptance(output_dir / "customer_acceptance.md", report, spec)
    _write_checksums(output_dir)
    return report


def _write_acceptance(path: Path, report: dict[str, Any], spec: dict[str, Any]) -> None:
    gates = "\n".join(
        f"- {name.replace('_', ' ').title()}: **{gate['status']}** "
        f"({gate['actual']:.1%} actual / {gate['threshold']:.1%} required)"
        for name, gate in report["quality_gates"].items()
    )
    counts = report["delivery_counts"]
    body = f"""# Dataset Acceptance Record — {report['project_id']}

**Customer:** {report['customer']}<br>
**Use case:** {spec['use_case']}<br>
**Classification:** {report['data_classification']}<br>
**Delivery status:** {report['delivery_status']}<br>

## Delivered scope

- {counts['patients']} longitudinal patients
- {counts['studies']} studies with {counts['reports']} linked final reports
- CSV tables, machine-readable QC report, row manifest, and SHA-256 checksums

## Acceptance gates

{gates}

## Known limitations

""" + "\n".join(f"- {item}" for item in report["limitations"]) + f"""

## Sign-off

Acceptance window: {spec['delivery']['acceptance_window_business_days']} business days after delivery.

| Role | Name | Decision | Date |
|---|---|---|---|
| BioStack Delivery Lead |  | Ready / Hold |  |
| Customer Technical Owner |  | Accept / Reject |  |
| Clinical Reviewer |  | Accept / Reject |  |
"""
    path.write_text(body, encoding="utf-8")


def _write_checksums(output_dir: Path) -> None:
    lines = []
    for path in sorted(output_dir.iterdir()):
        if path.is_file() and path.name != "checksums.sha256":
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {path.name}")
    (output_dir / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
