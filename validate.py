#!/usr/bin/env python3
"""Validator for MLS Imagery Policy Schema records (schema 0.1.0).

Checks FORMAT conformance only. A valid record is a well-formed record;
validation is NOT a legal or MLS compliance determination, and a valid
record can still describe a policy incorrectly. Standard library only.

LIMITATION: this is a lightweight checker that hand implements the
constraints used by schema 0.1.0. It is NOT a general JSON Schema
engine. It was cross validated against the jsonschema library on
2026-11-25 (verdict agreement on all shipped records and on an eight
case mutation battery). For standards grade validation, use the schema
file itself with a full JSON Schema validator.
Usage: python3 validate.py <record.json> [more.json ...]
Exit code 0 when every record is valid, 1 otherwise.
"""
import json, sys

STATUSES = {"confirmed", "conflicting", "unknown", "superseded", "unresolved_interpretation"}
PLACEMENTS = {"on_image", "adjacent_to_image", "public_remarks", "private_remarks",
              "photo_description", "link_url_or_qr_to_original", "unknown"}
SOURCE_TYPES = {"primary_rulebook", "board_staff_confirmation", "board_publication", "secondary"}
CONF_STATUSES = {"confirmed", "partially_confirmed", "unconfirmed"}

def check(rec):
    errs = []
    if not isinstance(rec, dict):
        return ["record is not a JSON object"]
    for key in ("schemaVersion", "board", "status", "sources", "requirements", "confirmation"):
        if key not in rec:
            errs.append(f"missing required field: {key}")
    if errs:
        return errs
    if rec["schemaVersion"] != "0.1.0":
        errs.append(f"schemaVersion must be '0.1.0', got {rec['schemaVersion']!r}")
    board = rec["board"]
    if not isinstance(board, dict) or not board.get("id") or not board.get("name"):
        errs.append("board requires non-empty id and name")
    if rec["status"] not in STATUSES:
        errs.append(f"status must be one of {sorted(STATUSES)}, got {rec['status']!r}")
    srcs = rec["sources"]
    if not isinstance(srcs, list) or not srcs:
        errs.append("sources must be a non-empty array")
    else:
        for i, s in enumerate(srcs):
            if s.get("type") not in SOURCE_TYPES:
                errs.append(f"sources[{i}].type invalid: {s.get('type')!r}")
            if not s.get("citation"):
                errs.append(f"sources[{i}].citation is required")
    req = rec["requirements"]
    if req.get("disclosureRequired") not in (True, False, "unknown"):
        errs.append("requirements.disclosureRequired must be true, false, or 'unknown'")
    for p in req.get("placement", []):
        if p not in PLACEMENTS:
            errs.append(f"requirements.placement value invalid: {p!r}")
    if req.get("originalImageRequired") not in (True, False, "unknown"):
        errs.append("requirements.originalImageRequired must be true, false, or 'unknown'")
    if req.get("onImageText") not in ("permitted", "prohibited", "unknown"):
        errs.append("requirements.onImageText must be permitted, prohibited, or unknown")
    conf = rec["confirmation"]
    if conf.get("status") not in CONF_STATUSES:
        errs.append(f"confirmation.status invalid: {conf.get('status')!r}")
    # Semantic rules: the format's honesty constraints.
    if rec["status"] == "confirmed" and conf.get("status") != "confirmed":
        errs.append("a record with status 'confirmed' requires confirmation.status 'confirmed'")
    if rec.get("conflicts") and rec["status"] not in ("conflicting", "unresolved_interpretation"):
        errs.append("a record with conflicts must have status 'conflicting' or 'unresolved_interpretation'")
    if rec["status"] == "superseded" and not rec.get("supersededBy"):
        errs.append("a superseded record must name its replacement in 'supersededBy'")
    return errs

def main(paths):
    bad = 0
    for path in paths:
        try:
            rec = json.load(open(path))
        except Exception as e:
            print(f"INVALID {path}: not parseable JSON ({e})"); bad += 1; continue
        errs = check(rec)
        if errs:
            bad += 1
            print(f"INVALID {path}:")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"VALID   {path} (format conformance only; not a compliance determination)")
    return 1 if bad else 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    sys.exit(main(sys.argv[1:]))
