# RadReady

**A customer-to-delivery simulator for longitudinal radiology datasets.**

RadReady turns an ambiguous AI-lab request into a versioned data contract, screens a synthetic multi-site dataset, builds a longitudinal cohort, quarantines defects, and emits an acceptance-ready delivery package. It is a compact portfolio project for clinical data delivery—not a clinical product.

> All records are deterministic synthetic data. No PHI, patient data, or proprietary BioStack data is used. This project is independent and unaffiliated with BioStack Platforms.

## Run the 30-second demo

Requirements: Python 3.11+. No third-party packages are required.

```bash
make demo
```

Then open [`artifacts/delivery/dashboard.html`](artifacts/delivery/dashboard.html) in a browser. The deterministic demo produces:

- 180 synthetic source patients across three fictional imaging providers
- 112 delivered longitudinal patients and 318 chest CT studies
- automated cohort, consent, license, report, metadata, and PHI-pattern gates
- quarantine evidence for seeded source defects
- a machine-readable QC report, acceptance record, manifest, and SHA-256 checksums

Run the validation suite with:

```bash
make test
```

## The customer scenario

A fictional frontier AI lab wants data to evaluate whether a model can detect change over time from adult chest CT reports. The ask sounds simple, but “longitudinal chest CT” leaves critical delivery questions unresolved: minimum follow-up, report status, consent, usage rights, metadata completeness, and acceptance thresholds.

[`config/customer_spec.json`](config/customer_spec.json) converts those unknowns into an executable contract. The contract selects adult, research-consented patients with at least two licensed chest CTs, final reports, and 90–1,095 days of follow-up.

## What it demonstrates

```text
Customer need
    ↓  clarify use case, cohort, rights, acceptance gates
Executable data contract
    ↓  evaluate metadata, linkage, consent, license, PHI patterns
Source qualification
    ↓  quarantine defects; preserve an audit trail
Longitudinal cohort
    ↓  package tables, manifest, QC evidence, checksums
Customer acceptance
```

| Role signal | Evidence in this repository |
|---|---|
| Translate customer needs | Executable [customer spec](config/customer_spec.json) and [scoping brief](docs/SCOPING_BRIEF.md) |
| Judge whether data is useful | Use-case-specific cohort and five measurable quality gates |
| Source and select providers | Weighted [provider scorecard](ops/provider_scorecard.csv) and [decision memo](ops/PROVIDER_DECISION.md) |
| Own QC and delivery | Deterministic pipeline, quarantine log, manifest, checksums, and sign-off record |
| Operate reliably | [Delivery playbook](docs/DELIVERY_PLAYBOOK.md) with owners, SLAs, severity, and escalation rules |
| Communicate crisply | Executive dashboard and [three-minute demo script](docs/DEMO_SCRIPT.md) |

## Deliberate defects

The generator seeds five realistic problem types: a missing accession token, a duplicate study UID, missing report links, a synthetic phone-number pattern in report text, and an orphan report. It also creates operational exclusions such as pending licenses, clinical-only consent, and preliminary reports.

The important behavior is not “finding bad rows.” RadReady keeps source defects separate from valid cohort exclusions, quarantines affected studies before selection, and records disposition without silently modifying the source.

## Delivery package

After `make demo`, `artifacts/delivery/` contains:

| Artifact | Customer purpose |
|---|---|
| `dashboard.html` | Go/no-go summary for clinical, technical, and business owners |
| `qc_report.json` | Machine-readable metrics, gates, exclusions, and limitations |
| `cohort_manifest.csv` | Study/report linkage, provenance, and record-level integrity hash |
| `patients.csv`, `studies.csv`, `reports.csv` | Minimal, selected delivery tables |
| `quarantine_log.csv` | Auditable defect disposition |
| `customer_acceptance.md` | Formal scope, thresholds, limitations, and sign-off |
| `checksums.sha256` | File-level delivery integrity |

## Quality model

Readiness is a transparent weighted score, while contractual acceptance remains gate-based. A high average can never hide a failed hard gate.

| Gate | Contract threshold | Why it matters |
|---|---:|---|
| Required metadata completeness | 98% | Data must be indexable and joinable |
| Study-to-report linkage | 98% | The evaluation unit needs both inputs |
| PHI-pattern scan pass | 99% | Pre-delivery privacy safeguard |
| Longitudinal coverage | 95% | Cohort must actually support change over time |
| License approval in delivery | 100% | Rights are non-negotiable |

## Design choices and boundaries

- **Synthetic first:** safe to publish and demo; it does not claim clinical validation.
- **Standard library only:** reproducible in a clean environment and easy for a reviewer to run.
- **Contract before pipeline:** quality is defined by the intended model workflow, not generic cleanliness.
- **Quarantine before cohorting:** prevents broken records from distorting selection or metrics.
- **Conservative privacy language:** regex screening is useful triage, not proof of HIPAA de-identification.
- **Metadata-only imaging scope:** pixel-level DICOM validation, annotation agreement, bias evaluation, and model benchmarking are named next steps rather than overstated features.

## Repository map

```text
config/customer_spec.json       executable customer contract
src/radready/synthetic.py       multi-site synthetic source generator
src/radready/pipeline.py        QC, quarantine, cohort, and packaging
src/radready/report.py          zero-dependency delivery dashboard
ops/                            provider selection evidence
docs/                           scoping, operating, and interview artifacts
tests/                          end-to-end contract tests
```

## Resume-ready framing

Use the bullets in [`docs/RESUME_BULLETS.md`](docs/RESUME_BULLETS.md), adjusting only after you have run the project and can defend each decision. The strongest interview story is the tradeoff: broad data volume was intentionally sacrificed to guarantee consent, usage rights, final-report linkage, and longitudinal fitness.
