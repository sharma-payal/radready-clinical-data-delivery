# Generated Data License and Provenance

## Clear license split

- **Software, documentation, configuration, and dashboard code:** MIT License, as stated in [`LICENSE`](LICENSE).
- **Tabular data generated solely by `src/radready/synthetic.py`:** dedicated under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
- **Third-party or external datasets:** none are included, downloaded, transformed, redistributed, or licensed by this repository.

To the extent Payal Sharma owns copyright and related database rights in the generated synthetic rows, those rights are waived under CC0 1.0 Universal. The canonical legal text is available from [Creative Commons](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en).

## Scope of the CC0 dedication

CC0 applies only to data produced by the repository’s generator without real-world source data. It does not grant rights in:

- patient, privacy, publicity, or personality rights;
- third-party datasets, terminology systems, images, annotations, or model outputs;
- names, logos, or trademarks of third parties;
- software code, which remains under MIT; or
- any future material added without an explicit provenance and license record.

The generated records are fictional, provided without warranty, and not intended for clinical use, diagnosis, treatment, regulatory submission, or claims about real populations.

## Provenance record

`config/data_rights_registry.json` is the machine-readable source-of-truth. It records synthetic-only mode, fictional providers, generator origin, rights basis, and license. `make audit` verifies each row against that registry before delivery.

The row-level `license_status` and consent values are deliberately simulated workflow conditions used to test exclusion logic. They do not describe the copyright status of the author-generated output or any real patient permission; CC0 governs the generated synthetic rows as described above.

Do not label external data “synthetic,” “de-identified,” “public,” or “open” as a substitute for reviewing its actual terms. Public accessibility does not necessarily grant redistribution, commercial use, model-training, derivative, or sublicensing rights.
