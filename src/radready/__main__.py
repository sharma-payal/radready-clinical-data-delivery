from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from .pipeline import run_delivery
from .report import render_dashboard
from .synthetic import generate_dataset


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW = ROOT / "data" / "raw"
DEFAULT_DELIVERY = ROOT / "artifacts" / "delivery"
DEFAULT_SPEC = ROOT / "config" / "customer_spec.json"


def main() -> None:
    parser = argparse.ArgumentParser(prog="radready", description="Clinical dataset delivery simulator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate = subparsers.add_parser("generate", help="create deterministic synthetic source data")
    generate.add_argument("--seed", type=int, default=42)
    subparsers.add_parser("deliver", help="run cohort selection, QC, and delivery packaging")
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
    if args.command in {"deliver", "demo"}:
        report = run_delivery(DEFAULT_RAW, DEFAULT_DELIVERY, DEFAULT_SPEC)
        render_dashboard(report, DEFAULT_DELIVERY / "dashboard.html")
        # Refresh checksums after the dashboard is added.
        from .pipeline import _write_checksums
        _write_checksums(DEFAULT_DELIVERY)
        print(
            f"Delivery {report['delivery_status']}: {report['delivery_counts']['patients']} patients, "
            f"{report['delivery_counts']['studies']} studies, readiness {report['readiness_score']}/100"
        )
        print(f"Dashboard: {DEFAULT_DELIVERY / 'dashboard.html'}")


if __name__ == "__main__":
    main()
