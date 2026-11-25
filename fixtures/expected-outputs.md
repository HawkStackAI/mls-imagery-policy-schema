# Fixtures and expected outputs

Run from the repository root. The test script `python3 fixtures/run_fixtures.py` checks all of these.

| File | Validator | Consumer output begins |
| --- | --- | --- |
| samples/crmls.json | VALID | "California Regional MLS (CRMLS): DISCLOSURE REQUIRED." |
| samples/bright-mls.json | VALID | "Bright MLS: DISCLOSURE REQUIRED." and includes "Do NOT put disclosure text on the image itself" |
| samples/canopy-mls.json | VALID | "Canopy MLS: DISCLOSURE REQUIRED." |
| samples/beaches-mls.json | VALID | "BeachesMLS: DISCLOSURE REQUIRED." including the board specific constraint "within the first 180 characters of the public remarks" (carried in `placementDetail`), plus the on-image prohibition line |
| samples/har.json | VALID | "Houston Association of REALTORS (HAR): DISCLOSURE REQUIRED." |
| fixtures/sabor-conflicting.json | VALID | "San Antonio Board of REALTORS (SABOR): CONFLICT FLAGGED." |
| fixtures/crmls-superseded.json | VALID | "California Regional MLS (CRMLS): SUPERSEDED." |
| fixtures/example-unknown.json | VALID | "Example Unverified MLS (synthetic fixture): INSUFFICIENT INFORMATION." |
| fixtures/invalid-record.json | INVALID (multiple errors) | not applicable |
