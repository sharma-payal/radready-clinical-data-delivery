# Privacy and Data Protection

## Current repository status

RadReady is a **synthetic-only software demonstration**. The repository contains no real patient records, protected health information (PHI), personally identifiable information, hospital exports, medical images, or third-party datasets.

All demo rows are created deterministically by `src/radready/synthetic.py`. Provider names are explicit placeholders (`Synthetic Provider A`, `B`, and `C`), patient keys are fabricated tokens, and the phone-number-shaped value is a fictional test pattern that is intentionally quarantined.

The committed dashboard contains only synthetic tokens, aggregate counts, and synthetic QC results. `data/raw/` and all generated delivery files except that dashboard are blocked by `.gitignore`.

## Enforced controls

- `config/data_rights_registry.json` fixes the project in `synthetic_only` mode and registers every fictional source.
- Every source row must declare `synthetic_flag=true` and `data_origin=project_generator`.
- Every study must reference an approved rights-registry entry.
- Direct-identifier column names cause the governance audit to fail.
- Any external dataset entry causes this public demo to fail closed.
- Free-text PHI-like patterns are quarantined before cohort selection.
- CI runs both contract tests and the complete delivery workflow.

Run the privacy and rights preflight with:

```bash
make audit
```

## What this does not claim

This project does **not** claim HIPAA compliance, HIPAA de-identification certification, regulatory approval, clinical validation, or fitness for patient care. A regular expression scan is only a first-pass control. Synthetic data governance does not demonstrate that a process is adequate for real clinical data.

HHS recognizes Safe Harbor and Expert Determination as methods for de-identifying PHI under the HIPAA Privacy Rule. Selection and documentation of an applicable method must be performed by the data-owning covered entity or its authorized experts. The DICOM standard also warns that applying an attribute confidentiality profile does not by itself guarantee that the complete information object is de-identified, particularly when pixel data may contain identifying information.

## Rule for future real-world data

Do not add real, coded, limited, de-identified, or identifiable clinical data to this public repository. Before any non-synthetic data is accessed, copied, transformed, or delivered, the responsible organization must document, as applicable:

1. authority to disclose and receive the data;
2. an executed data use agreement, license, and/or business associate agreement;
3. the permitted purpose, recipients, geography, retention, deletion, redistribution, derivative-model, and commercialization terms;
4. an institutional determination regarding human-subjects research, consent, authorization, exemption, or waiver;
5. the selected de-identification method and evidence, including free text, DICOM metadata, overlays, burned-in pixels, and longitudinal-linkage risk;
6. security risk analysis, access controls, audit logging, encryption, incident response, and breach-notification responsibilities;
7. privacy-law review for every relevant jurisdiction; and
8. written approval from the designated privacy, security, legal, and data-owner roles.

The operational checklist is in [`docs/DATA_RIGHTS_CHECKLIST.md`](docs/DATA_RIGHTS_CHECKLIST.md). Official references are collected in [`docs/LEGAL_SOURCES.md`](docs/LEGAL_SOURCES.md).

## Data minimization and incident handling

Use the minimum fields necessary for the documented purpose. Never place secrets, credentials, linkage keys, re-identification keys, or real health data in issues, pull requests, CI logs, screenshots, or example files.

If sensitive data is accidentally introduced, stop distribution, restrict access, preserve incident evidence, notify the responsible privacy/security owner, rotate exposed credentials, and remove the data from both current files and Git history using an approved incident process. Deleting only the latest file is insufficient.

This policy is technical documentation, not legal advice. Real clinical-data use requires review by qualified privacy and legal professionals.
