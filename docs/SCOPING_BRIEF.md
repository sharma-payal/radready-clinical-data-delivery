# Customer Scoping Brief — BS-RAD-001

## One-sentence outcome

Deliver a reproducible adult chest CT cohort that lets a frontier AI lab evaluate report-level longitudinal change detection—not train a diagnostic model or support patient care.

## What I would clarify in the first customer call

1. **Decision being evaluated:** Is success classification, summarization, temporal reasoning, or retrieval? This demo assumes temporal reasoning from paired reports.
2. **Unit of evaluation:** One study, a study pair, or a full patient timeline? This demo delivers complete eligible timelines with stable patient tokens.
3. **Target findings:** Are nodules, emphysema, treatment response, and incidental findings equally relevant? This remains a label-design decision.
4. **Reference standard:** Radiologist report, double-read adjudication, pathology, or follow-up outcome? This demo provides final reports but makes no ground-truth claim.
5. **Population constraints:** Age, geography, care setting, scanner mix, contrast, and exclusions. This demo requires adults and records source site for subgroup analysis.
6. **Rights and privacy:** Permitted use, retention, derivative models, geography, and deletion obligations. This demo blocks pending licenses and non-research consent.
7. **Acceptance:** Minimum volume, completeness, linkage, privacy scan, longitudinal interval, and rejection/remediation workflow.

## Executed assumptions

| Dimension | Decision | Reason |
|---|---|---|
| Modality/anatomy | CT / chest | Matches the temporal report-evaluation scenario |
| Age | 18+ | Limits pediatric distribution shift for the first delivery |
| Timeline | ≥2 studies, 90–1,095 days | Avoids near-duplicate episodes and excessively stale follow-up |
| Report | Final signed report required | Preliminary text is operationally unstable |
| Consent | Research use required | Conservative use limitation |
| License | Approved at delivery | Rights are a hard gate, never a weighted tradeoff |
| Data format | Normalized CSV + JSON QC + checksums | Inspectable without specialized infrastructure |

## Explicitly out of scope

- Clinical performance or safety claims
- DICOM pixel transfer and image-header de-identification
- Finding-level labels or radiologist adjudication
- Hospital integration, BAAs, or production security controls
- Representativeness claims across race, ethnicity, geography, scanners, or disease prevalence

## Change-control rule

Any change to intended use, cohort, labels, rights, or acceptance thresholds creates a new customer-spec version and requires an impact estimate before pipeline changes. Delivery does not begin against verbal scope.
