from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .governance import audit_privacy_and_rights
from .pipeline import run_delivery, write_checksums
from .report import render_dashboard
from .synthetic import generate_dataset


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW = ROOT / "data" / "raw"
DEFAULT_DELIVERY = ROOT / "artifacts" / "delivery"
DEFAULT_SPEC = ROOT / "config" / "customer_spec.json"
DEFAULT_REGISTRY = ROOT / "config" / "data_rights_registry.json"


def main() -> None:
    parser = argparse.ArgumentParser(prog="radready", description="Clinical dataset delivery simulator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate = subparsers.add_parser("generate", help="create deterministic synthetic source data")
    generate.add_argument("--seed", type=int, default=42)
    subparsers.add_parser("deliver", help="run cohort selection, QC, and delivery packaging")
    subparsers.add_parser("audit", help="verify synthetic provenance, privacy policy, and data rights")
    subparsers.add_parser("demo", help="regenerate data and run the complete delivery workflow")
    subparsers.add_parser("clean", help="remove generated synthetic data and delivery artifacts")
    args = parser.parse_args()

    if args.command == "clean":
        for path in (DEFAULT_RAW, DEFAULT_DELIVERY):
            if path.exists():
                shutil.rmtree(path)
        print("Removed generated demo data and artifacts.")
        return

    if args.command in {"generate", "demo"}:
        seed = getattr(args, "seed", 42)
        counts = generate_dataset(DEFAULT_RAW, seed=seed)
        print(f"Generated synthetic source: {counts}")
    if args.command == "audit":
        if not DEFAULT_RAW.exists():
            generate_dataset(DEFAULT_RAW, seed=42)
        audit = audit_privacy_and_rights(DEFAULT_RAW, DEFAULT_REGISTRY)
        DEFAULT_DELIVERY.mkdir(parents=True, exist_ok=True)
        (DEFAULT_DELIVERY / "governance_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
        write_checksums(DEFAULT_DELIVERY)
        print(
            f"Governance {audit['status']}: {sum(audit['rows_checked'].values())} rows, "
            f"{audit['external_dataset_count']} external datasets, {audit['generated_data_license']} data license"
        )
    if args.command in {"deliver", "demo"}:
        report = run_delivery(DEFAULT_RAW, DEFAULT_DELIVERY, DEFAULT_SPEC, DEFAULT_REGISTRY)
        render_dashboard(report, DEFAULT_DELIVERY / "dashboard.html")
        # Refresh checksums after the dashboard is added.
        write_checksums(DEFAULT_DELIVERY)
        print(
            f"Delivery {report['delivery_status']}: {report['delivery_counts']['patients']} patients, "
            f"{report['delivery_counts']['studies']} studies, readiness {report['readiness_score']}/100"
        )
        print(f"Dashboard: {DEFAULT_DELIVERY / 'dashboard.html'}")


if __name__ == "__main__":
    main()
