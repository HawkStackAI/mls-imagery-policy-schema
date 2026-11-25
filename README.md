# MLS Imagery Policy Schema

An open specification for representing real estate imagery policies, virtual staging disclosures and image alteration requirements in machine-readable form.

Developed and maintained by RELTO.

This is not an official MLS or RESO standard, and nothing here implies adoption or endorsement by any MLS, association, or standards body. It is a working format published by its originating maintainer so that adoption, if it comes, is earned by usefulness.

## Why this exists

Every platform that publishes listing photos has to answer the same questions, board by board: Is disclosure required for an altered image? Where must it appear? Is text on the image allowed, required, or prohibited? Must the original sit next to the altered version? Today those answers live in rulebooks, PDFs, and staff emails, re-interpreted by every engineering team that touches listing media.

This schema gives those answers one machine-readable shape, including the parts that are not settled: exceptions, conflicting sources, unclear effective dates, unknown values, and confirmation status are represented explicitly instead of being flattened into a boolean.

## Five minute quick start

Run from the repository root:

```bash
# 1. Validate a record (format conformance only; see the warning below)
python3 validate.py samples/beaches-mls.json

# 2. Turn a record into a disclosure decision
python3 examples/consume_policy.py samples/beaches-mls.json

# 3. Run the full fixture suite (valid, conflicting, superseded, unknown, invalid)
python3 fixtures/run_fixtures.py
```

No dependencies. Python 3 standard library only.

## The one rule

A record's `status` describes how much the record itself can be trusted, and consuming applications must branch on it:

| Policy status | Expected application behavior |
| --- | --- |
| `confirmed` | Generate the applicable disclosure |
| `conflicting` | Flag the conflict for resolution; do not generate instructions |
| `unknown` | Return insufficient information; do not guess |
| `superseded` | Identify and use the newer version |
| `unresolved_interpretation` | Require manual review |

Never generate definitive disclosure instructions from an unresolved policy. And when a record carries a `placementDetail` (a board specific constraint the placement enum cannot express, such as a character limit inside the remarks), preserve it verbatim in the generated instruction; dropping it produces an under-specified disclosure. The example in `examples/consume_policy.py` implements exactly this table and is the reference behavior.

## What is in this repository

- `schema/policy-record.schema.json` — the JSON Schema (version 0.1.0, stable identifier in the file's `$id`).
- `samples/` — five complete records for real boards (CRMLS, Bright MLS, Canopy MLS, BeachesMLS, HAR), each with its sources and confirmation status, including honestly unknown fields.
- `fixtures/` — records exercising every status path, including a real citation conflict from the maintainer's own corpus (SABOR), a superseded record (an outdated CRMLS FAQ), a synthetic unknown board, and a deliberately invalid record, each with expected outputs in `fixtures/expected-outputs.md`.
- `validate.py` — a dependency-free format validator.
- `examples/consume_policy.py` — the minimal working implementation described above.
- `CHANGELOG.md` — what maintaining current policy records actually looks like, in dated changes.
- `docs/integration.md` — how this format relates to maintained policy data and commercial services.
- `AGENTS.md` — implementation guidance written for AI coding agents.

## Validation is not compliance

The validator checks that a record is well formed. It does not and cannot determine whether a listing complies with an MLS's rules. A valid record can still describe a policy incorrectly; that is why every record carries its sources and confirmation status, and why consuming applications must honor the status table above.

## The maintained data behind the format

This repository ships the format and five sample records. The policies themselves change: boards amend rules, issue citation policies, and supersede their own guidance (see the changelog). RELTO maintains a continuously updated database of these records across US boards as a commercial service, with automated change notifications and disclosure generation built on this same schema. You can maintain hundreds of MLS policy records yourself, or RELTO can maintain them for you. See `docs/integration.md`.

## Licensing

Software (schema, validator, example code): Apache License 2.0, see `LICENSE`.

Sample records: the facts in each record are published with their sources cited in the record itself. The Apache license covers the software; it does not by itself resolve rights in any third party source material a record cites or links. Rule text is paraphrased and cited, not reproduced.

## Maintainer

RELTO (relto.app) — AI virtual staging that doesn't change the house, and the research program behind The Staging Report. Issues and corrections are welcome; a correction with a primary source is the fastest way to get a record changed.

## Limitations, stated plainly

- **RESO mapping is unfinished.** This schema does not yet map its jurisdiction and listing identifiers to RESO Data Dictionary conventions. That mapping is future work, recorded here as a limitation. Nothing in this repository claims RESO compatibility or alignment.
- **The bundled validator is a lightweight checker, not a JSON Schema engine.** `validate.py` hand implements the constraints this schema uses (required fields, enums, types, and the semantic honesty rules described in AGENTS.md). It was cross checked on November 25, 2026 against the established `jsonschema` library (Draft 2020-12): the schema itself is a valid Draft 2020-12 schema, both validators agreed on the validity verdict for every shipped record and fixture, and both rejected all eight records in a mutation battery (bad enums, missing fields, wrong types, empty sources). Error granularity differs: the reference validator itemizes some malformed records more finely. For standards grade validation, run the schema through a full JSON Schema validator; `validate.py` exists so the quick start needs no dependencies.
- **Five sample boards are samples.** Coverage is the maintained service's job, not this repository's.
