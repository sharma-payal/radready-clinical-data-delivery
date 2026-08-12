# Security Policy

## Supported scope

This repository is a portfolio demonstration and does not operate a production service. Security reports concerning the current `main` branch are welcome.

## Never submit health data

Do not include real patient information, screenshots, medical images, access tokens, credentials, or confidential provider/customer material in a public issue, pull request, discussion, test fixture, or CI log.

If a report requires sensitive details, use GitHub private vulnerability reporting when available or contact the repository owner through an agreed private channel before sharing evidence. Provide only the minimum information necessary.

## Accidental sensitive-data exposure

Treat any suspected real-health-data commit as a privacy incident:

1. stop further sharing and automation;
2. restrict repository and artifact access where authorized;
3. notify the responsible privacy/security owner immediately;
4. preserve incident evidence without copying sensitive content into new systems;
5. remove data from current files and Git history through an approved process;
6. rotate exposed secrets and invalidate links; and
7. assess contractual and legal notification obligations with qualified counsel.

Never assume that deleting a file in a later commit removes it from clones, caches, artifacts, or history.

## Secrets

The project requires no API keys, cloud credentials, or clinical-system access. CI permissions are read-only. Do not add secrets to the repository; use an approved secret manager for any future integration.
