# Clinical Dataset Delivery Playbook

## Operating cadence

| Stage | Exit criterion | Directly responsible | Customer touchpoint |
|---|---|---|---|
| Discover | Intended use and decision owner documented | Clinical Data Lead | 45-minute scoping call + written recap within 4 hours |
| Contract | Cohort, rights, schema, gates, and acceptance signed | Data Lead + customer technical owner | Versioned data contract |
| Source | Provider evidence room complete | Provider owner | Weekly capacity/risk update |
| Pilot | Representative 1–5% sample clears hard gates | Data engineering + clinical reviewer | Pilot readout and go/no-go |
| Produce | Frozen pipeline runs on full source | Data engineering | Daily critical-risk update |
| Accept | Checksums verified; customer signs acceptance | Clinical Data Lead | Delivery review + 5-day acceptance window |
| Learn | Defects and scope changes captured | Clinical Data Lead | Retrospective within 3 business days |

## Severity and response

| Severity | Example | Acknowledge | Action |
|---|---|---:|---|
| S0 — Privacy/rights | Suspected PHI leak or unlicensed records delivered | 15 min | Stop transfer, preserve evidence, notify security/legal owners, rotate package |
| S1 — Acceptance blocker | Broken manifest, material cohort mismatch, corrupted files | 30 min | Name incident owner, update customer every 2 hours, issue corrected delivery |
| S2 — Material quality | Threshold at risk, provider delay, systematic missing metadata | 4 hours | Quantify impact and propose scope/time tradeoffs |
| S3 — Routine | Clarification or isolated remediable defect | 1 business day | Track in decision log and next status update |

## Delivery go/no-go checklist

- Customer spec is versioned and scope owner is named.
- Governance audit confirms synthetic provenance for this demo; any external data blocks delivery.
- Provider rights cover intended use, geography, retention, and derivatives.
- Patient and study counts match the manifest.
- Every delivered study has a qualifying patient, final report, consent, and approved license.
- Hard quality gates pass; exceptions have written customer approval.
- Quarantined rows are absent from delivered tables and present in the defect log.
- File and row checksums reproduce.
- Clinical reviewer and customer technical owner have a named sign-off path.
- Limitations are visible in the QC report and acceptance record.
- Software and dataset licenses are identified separately and match the rights registry.

## Status update template

**Decision/status:** Green / Amber / Red — one sentence.<br>
**Delivered since last update:** measurable outputs.<br>
**Next milestone:** owner and UTC deadline.<br>
**Risks:** impact, probability, mitigation, decision needed.<br>
**Customer ask:** one clear action with a deadline.
