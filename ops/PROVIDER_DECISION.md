# Provider Selection Memo — Longitudinal Chest CT Pilot

## Recommendation

Start a representative 1–5% pilot with **Bay Imaging** (fictional), conditioned on independent validation of its de-identification process. Keep Lakeview as the technical-quality fallback only after derivative-model rights are resolved in writing.

## Scoring method

Each provider is scored 1–5 on six dimensions. Weighted total = clinical fit × 25% + rights readiness × 20% + metadata quality × 15% + de-identification × 15% + longitudinal depth × 15% + delivery operations × 10%, normalized to 100.

Rights readiness ranks nearly as high as clinical fit because unusable rights make technically excellent data commercially irrelevant. Price is intentionally absent until minimum quality and rights thresholds pass; then it becomes a negotiation variable rather than a substitute for fitness.

## Pilot evidence request

- Data lineage from acquisition system to export
- Modality/body-part counts and 12-month longitudinal overlap
- DICOM tag completeness and burned-in-pixel risk assessment
- Report finalization and amendment rates
- Consent/authorization basis and permitted-use matrix
- De-identification method, validation evidence, and residual-risk owner
- Sample manifest with stable patient/study keys
- Historical SLA, re-delivery rate, and named escalation contacts across time zones

## Negotiation positions

1. Accept volume bands, but do not waive patient-level linkage or approved rights.
2. Tie payment milestones to pilot acceptance and batch-level quality gates.
3. Require remediation or replacement for systematic defects; define isolated-defect tolerance in the contract.
4. Record deletion, derivative-use, geography, and breach-notification obligations explicitly.
5. Do not promise the customer a full-delivery date before pilot evidence clears.

## Decision log

| Decision | Owner | Trigger to revisit |
|---|---|---|
| Bay Imaging selected for pilot | Clinical Data Lead | De-identification evidence fails review |
| Lakeview placed on rights hold | Commercial/legal owner | Executed derivative-rights addendum |
| Metro used only for gap fill | Sourcing owner | Cohort diversity or volume misses target |
