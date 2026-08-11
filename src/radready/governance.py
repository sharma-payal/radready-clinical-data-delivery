from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class GovernanceError(RuntimeError):
    """Raised when privacy or data-rights preflight fails closed."""


DIRECT_IDENTIFIER_HEADERS = {
    "address",
    "date_of_birth",
    "dob",
    "email",
    "first_name",
    "last_name",
    "medical_record_number",
    "mrn",
    "name",
    "phone",
    "social_security_number",
    "ssn",
}


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def audit_privacy_and_rights(raw_dir: Path, registry_path: Path) -> dict[str, Any]:
    """Fail closed unless every source row is registered, synthetic, and permissioned."""
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    issues: list[dict[str, str]] = []
    providers = {row["provider_id"]: row for row in registry.get("providers", [])}

    if registry.get("project_mode") != "synthetic_only":
        issues.append({"code": "project_mode_not_synthetic_only", "detail": "Registry must use synthetic_only mode."})
    if registry.get("external_datasets"):
        issues.append({"code": "external_dataset_registered", "detail": "This public demo permits no external datasets."})
    if registry.get("generated_data_license") != "CC0-1.0":
        issues.append({"code": "data_license_missing", "detail": "Generated data must be explicitly dedicated under CC0-1.0."})

    for provider_id, provider in providers.items():
        if provider.get("is_fictional") is not True:
            issues.append({"code": "provider_not_fictional", "detail": provider_id})
        if provider.get("status") != "approved":
            issues.append({"code": "provider_rights_not_approved", "detail": provider_id})
        if provider.get("rights_basis") != "author_generated_synthetic":
            issues.append({"code": "provider_rights_basis_invalid", "detail": provider_id})

    row_counts: Counter[str] = Counter()
    observed_sources: set[str] = set()
    for table_name in ("patients", "studies", "reports"):
        path = raw_dir / f"{table_name}.csv"
        headers, rows = _read_csv(path)
        row_counts[table_name] = len(rows)
        prohibited_headers = sorted(set(headers) & DIRECT_IDENTIFIER_HEADERS)
        if prohibited_headers:
            issues.append({
                "code": "direct_identifier_column_present",
                "detail": f"{table_name}: {','.join(prohibited_headers)}",
            })
        for row_number, row in enumerate(rows, start=2):
            if row.get("synthetic_flag") != "true":
                issues.append({"code": "record_not_marked_synthetic", "detail": f"{table_name}:{row_number}"})
            if row.get("data_origin") != "project_generator":
                issues.append({"code": "unapproved_data_origin", "detail": f"{table_name}:{row_number}"})
            source_site = row.get("source_site")
            if not source_site:
                continue
            observed_sources.add(source_site)
            provider = providers.get(source_site)
            if provider is None:
                issues.append({"code": "unregistered_source", "detail": f"{table_name}:{row_number}:{source_site}"})
                continue
            if row.get("rights_basis") and row["rights_basis"] != provider["rights_basis"]:
                issues.append({"code": "rights_basis_mismatch", "detail": f"{table_name}:{row_number}"})
            if row.get("rights_registry_id") and row["rights_registry_id"] != provider["rights_registry_id"]:
                issues.append({"code": "rights_registry_mismatch", "detail": f"{table_name}:{row_number}"})

    report = {
        "status": "PASS" if not issues else "BLOCKED",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "classification": registry.get("classification"),
        "project_mode": registry.get("project_mode"),
        "software_license": registry.get("software_license"),
        "generated_data_license": registry.get("generated_data_license"),
        "external_dataset_count": len(registry.get("external_datasets", [])),
        "registered_sources": sorted(providers),
        "observed_sources": sorted(observed_sources),
        "rows_checked": dict(row_counts),
        "issues": issues,
        "boundary": "This audit proves repository policy conformance, not regulatory compliance.",
    }
    if issues:
        summary = "; ".join(f"{issue['code']} ({issue['detail']})" for issue in issues[:8])
        raise GovernanceError(f"Privacy and rights preflight blocked delivery: {summary}")
    return report
