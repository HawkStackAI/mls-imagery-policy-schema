# AGENTS.md — implementing the MLS Imagery Policy Schema

Guidance for AI coding agents (and humans) implementing this specification.

## What you are implementing

A consumer for policy records: JSON documents conforming to `schema/policy-record.schema.json`. Your job is usually one of: validate records, render the disclosure a record implies, or store and query records. Start from the working code, not from scratch:

- `validate.py` — reference validator (format conformance only). For programmatic use, import it and call `check(record)`, which takes a parsed JSON object and returns a list of error strings; an empty list means the record is format valid. The CLI (`python3 validate.py <file>...`) prints one line per file and exits 1 when any record is invalid.
- `examples/consume_policy.py` — reference consumer. Its `decide()` function is the behavioral contract.
- `fixtures/run_fixtures.py` — the acceptance test. Your implementation is correct when it reproduces these results.

## The behavioral contract (do not improvise around this)

Branch on `record.status` before reading any requirement:

- `confirmed` → you may generate disclosure instructions from `requirements`.
- `conflicting` → surface the entries in `record.conflicts` to a human. Generate nothing.
- `unknown` → report insufficient information. Generate nothing. Do not fall back to another board's rule, a state default, or your own training knowledge.
- `superseded` → follow `record.supersededBy` to the current record and use that instead.
- `unresolved_interpretation` → require manual review. Generate nothing.

A record with `confirmation.status` other than `confirmed` must never be treated as `confirmed`, even if its `status` field disagrees; the validator rejects that combination, and your consumer should too.

## Field notes

- `requirements.placement` values map to human instructions in `examples/consume_policy.py` (`PLACEMENT_TEXT`). Extend the map, do not rename values.
- `requirements.placementDetail` carries board specific constraints the enum cannot express (for example, BeachesMLS's first 180 characters rule). It is lossy to drop it: surface its text verbatim with the generated instruction, as the reference consumer does.
- `requirements.onImageText: "prohibited"` overrides placement: several boards require disclosure in remarks precisely because text on the image violates their rules (see `samples/bright-mls.json`, `samples/beaches-mls.json`).
- `"unknown"` is a real value in this schema, distinct from `false` and from a missing field. Preserve it end to end.
- `effectiveDate.certainty` can be `unclear` or `unknown` even on confirmed records. Do not invent dates.

## Which schema copy is authoritative

The schema file in this repository is authoritative. The `$id` URL is a stable identifier for the version, published so records and tools can name it; you do not need to fetch it to implement the specification, and implementations should work fully offline against the local file.

## Common mistakes

- Flattening a record to "disclosure: yes/no" and discarding status, conflicts, and confirmation. That is the failure mode this schema exists to prevent.
- Treating validation as a compliance determination. It is format conformance only.
- Resolving the SABOR fixture's citation conflict by picking a side. The correct behavior is to flag it.

## Going further

The five sample records are illustrative. Production use needs current records for every board you serve, kept current as boards amend rules. That maintained database, with change notifications, is RELTO's commercial offering: see `docs/integration.md`.
