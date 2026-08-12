# Clinical Data Rights and Privacy Gate

This checklist is for a future real-world provider engagement. It is intentionally stricter than the synthetic demo and should be completed by named organizational owners before any data transfer. It is not legal advice.

## Gate 1 — Source authority

- Legal identity of provider and data owner verified.
- Provider documents how the data was collected and its authority to disclose it.
- Chain of title covers upstream systems, subcontractors, annotations, reports, pixels, and terminology assets.
- No brokered or scraped data is accepted without direct evidence of rights.
- Institutional privacy/legal owner is named.

**Exit:** written source-authority approval.

## Gate 2 — Permitted use

- Executed agreement identifies dataset, parties, purpose, and recipients.
- Terms cover research, evaluation, model training, post-training, human review, benchmarking, and production separately.
- Commercial use, redistribution, sublicensing, publication, derivative datasets, model weights, and generated outputs are explicit.
- Geography, cross-border transfer, retention, deletion, audit, breach, subcontractor, and termination obligations are explicit.
- BAA, DUA, license, or other required instrument is executed before transfer.

**Exit:** machine-readable rights matrix matches executed documents; legal owner signs off.

## Gate 3 — Research and patient authority

- Authorized institutional reviewer determines whether the activity is human-subjects research.
- Consent, HIPAA authorization, broad consent, IRB approval, exemption, waiver, or another basis is documented as applicable.
- Restrictions on future use, recontact, return of results, and withdrawal are mapped to records.
- Vulnerable populations and sensitive conditions receive specific review.

**Exit:** institutional research/privacy determination on file.

## Gate 4 — De-identification and re-identification risk

- HIPAA method is documented as Safe Harbor or Expert Determination when HIPAA applies.
- Free text, filenames, paths, manifests, headers, and embedded objects are included in scope.
- DICOM Basic Application Level Confidentiality Profile and selected options are documented.
- Pixel review covers burned-in text and recognizable features.
- Longitudinal date/UID transformation preserves only what the use case needs.
- Linkage keys and re-identification mappings are segregated and access-controlled.
- Recipient context and linkage attacks are considered; re-identification is contractually prohibited.
- Residual-risk evidence has an owner and review date.

**Exit:** documented de-identification decision plus independent validation.

## Gate 5 — Security and delivery

- Data-flow diagram, asset inventory, and risk analysis are current.
- Least privilege, MFA, encryption in transit/at rest, audit logs, backups, and key management are verified.
- Approved transfer channel and named recipients are tested.
- No PHI enters source control, public issue trackers, general chat, or CI logs.
- Batch manifest, hashes, record counts, quarantine evidence, and deletion confirmation are produced.
- Incident contacts and contractual notification clocks are tested across time zones.

**Exit:** security owner approves transfer; customer verifies receipt.

## Rights matrix minimum fields

| Field | Example decision |
|---|---|
| Data owner / discloser | Named legal entities |
| Data elements | Reports, metadata, pixels, annotations |
| Purpose | Evaluation only / training / deployment |
| Recipients | Named customer and approved subprocessors |
| Territory | Allowed processing and access countries |
| Derivatives | Cohorts, labels, embeddings, weights, outputs |
| Commercialization | Allowed / prohibited / approval required |
| Redistribution | None / named parties / aggregate only |
| Retention and deletion | Time limit, backups, attestations |
| De-identification basis | Safe Harbor / Expert Determination / other |
| Research basis | IRB/consent/authorization determination |
| Incident duties | Owner, clock, channel, required evidence |

If any field is unknown, the dataset remains **BLOCKED**—volume or customer urgency does not override the gate.
