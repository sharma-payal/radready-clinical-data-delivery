# Three-Minute Demo Script

## 0:00–0:30 — Frame the customer problem

“The customer asked for longitudinal chest CT data. That phrase is not a specification, so I made the intended evaluation workflow executable: adult patients, at least two exams, final reports, a meaningful follow-up window, research consent, approved rights, and explicit acceptance gates.”

Open `config/customer_spec.json`.

## 0:30–1:15 — Show judgment, not just plumbing

“Quality depends on use. Report linkage is critical for this temporal-reasoning evaluation; pixel quality would be critical for an imaging model. License approval is a hard gate because no weighted quality score can compensate for missing rights.”

Mention `docs/SCOPING_BRIEF.md` and `ops/PROVIDER_DECISION.md`.

## 1:15–2:15 — Run and inspect

```bash
make demo
```

Open `artifacts/delivery/dashboard.html`.

Point out:

- the source-to-delivery cohort funnel;
- actual versus contracted quality gates;
- seeded defects caught before cohort selection;
- sample patient timelines;
- visible limitations and synthetic-data classification.

Then open `quarantine_log.csv` and `cohort_manifest.csv` to show that the executive summary has row-level evidence.

## 2:15–3:00 — Close on ownership

“I treated delivery as a customer outcome, not a CSV export. The package includes an acceptance record, defect disposition, row and file integrity hashes, and an escalation playbook. Next, I would validate a 1–5% provider pilot, add DICOM header/pixel QC, and define clinician-adjudicated labels only after the customer confirms the model decision.”

## Likely interview questions

**Why not maximize cohort size?** Because research consent, usage rights, final reports, and timeline fitness are part of the product. Volume without usability is misleading.

**Is the PHI scanner sufficient?** No. It is deliberately described as first-pass triage. Production delivery needs an agreed de-identification standard, expert validation, image-header/pixel review, and contractual controls.

**What would break at scale?** In-memory CSV processing, manual provider evidence review, and simplistic terminology normalization. I would move computation to a warehouse, version schemas in a registry, and make gates observable by provider and batch.
