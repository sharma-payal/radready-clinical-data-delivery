from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


PATIENT_FIELDS = ["patient_token", "age", "sex", "state", "consent", "source_site"]
STUDY_FIELDS = [
    "study_uid", "patient_token", "study_date", "modality", "body_part",
    "accession_token", "description", "images_count", "slice_thickness_mm",
    "contrast", "source_site", "license_status",
]
REPORT_FIELDS = ["report_id", "study_uid", "report_text", "impression", "signed_status"]


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_dataset(output_dir: Path, seed: int = 42, patient_count: int = 180) -> dict[str, int]:
    """Generate deterministic, fully synthetic clinical data with known QC defects."""
    rng = random.Random(seed)
    patients: list[dict[str, object]] = []
    studies: list[dict[str, object]] = []
    reports: list[dict[str, object]] = []
    sites = ["Bay Imaging", "Lakeview Radiology", "Metro Diagnostics"]
    base_date = date(2022, 1, 1)
    study_counter = 0

    for index in range(patient_count):
        patient_token = f"P{index + 1:04d}"
        site = sites[index % len(sites)]
        is_target = index < int(patient_count * 0.72)
        patients.append({
            "patient_token": patient_token,
            "age": rng.randint(18, 88) if index != patient_count - 1 else 16,
            "sex": rng.choice(["F", "M", "X"]),
            "state": rng.choice(["CA", "TX", "NY", "WA", "IL"]),
            "consent": "research" if index % 17 else "clinical_only",
            "source_site": site,
        })

        study_total = rng.randint(2, 4) if is_target else rng.randint(1, 3)
        first_date = base_date + timedelta(days=rng.randint(0, 500))
        for sequence in range(study_total):
            study_counter += 1
            if is_target:
                modality, body_part = "CT", "CHEST"
                study_date = first_date + timedelta(days=sequence * rng.randint(105, 230))
                description = rng.choice(["CT CHEST W CONTRAST", "CT CHEST WO CONTRAST", "LOW DOSE CHEST CT"])
            else:
                modality, body_part = rng.choice([("MR", "BRAIN"), ("XR", "CHEST"), ("CT", "ABDOMEN")])
                study_date = first_date + timedelta(days=sequence * rng.randint(20, 90))
                description = f"{modality} {body_part}"

            study_uid = f"2.25.{seed}{study_counter:08d}"
            studies.append({
                "study_uid": study_uid,
                "patient_token": patient_token,
                "study_date": study_date.isoformat(),
                "modality": modality,
                "body_part": body_part,
                "accession_token": f"A{study_counter:07d}",
                "description": description,
                "images_count": rng.randint(80, 420) if modality == "CT" else rng.randint(2, 80),
                "slice_thickness_mm": rng.choice([1.0, 1.25, 2.5, 5.0]) if modality == "CT" else "",
                "contrast": "Y" if "W CONTRAST" in description else "N",
                "source_site": site,
                "license_status": "approved" if index % 19 else "pending",
            })
            finding = rng.choice(["stable pulmonary nodules", "no acute cardiopulmonary process", "mild emphysema"])
            reports.append({
                "report_id": f"R{study_counter:07d}",
                "study_uid": study_uid,
                "report_text": f"Synthetic exam. Findings demonstrate {finding}.",
                "impression": finding.capitalize() + ".",
                "signed_status": "final" if study_counter % 31 else "preliminary",
            })

    # Seed auditable failure modes that a realistic delivery workflow must catch.
    studies[4]["accession_token"] = ""
    studies.append(dict(studies[11]))  # duplicate StudyInstanceUID
    reports[19]["report_text"] += " Callback: 415-555-0134."  # synthetic PHI-like pattern
    missing_report_uids = {studies[450]["study_uid"], studies[451]["study_uid"]}
    reports = [report for report in reports if report["study_uid"] not in missing_report_uids]
    reports.append({
        "report_id": "R-ORPHAN",
        "study_uid": "2.25.999999999",
        "report_text": "Synthetic orphan report.",
        "impression": "No linked study.",
        "signed_status": "final",
    })

    _write_csv(output_dir / "patients.csv", PATIENT_FIELDS, patients)
    _write_csv(output_dir / "studies.csv", STUDY_FIELDS, studies)
    _write_csv(output_dir / "reports.csv", REPORT_FIELDS, reports)
    return {"patients": len(patients), "studies": len(studies), "reports": len(reports)}
