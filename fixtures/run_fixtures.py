#!/usr/bin/env python3
"""Fixture test: validator verdicts and consumer behavior for every shipped record."""
import glob, json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from validate import check
from examples.consume_policy import decide

fails = []
def expect(cond, label):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond: fails.append(label)

for path in sorted(glob.glob(f"{ROOT}/samples/*.json")):
    rec = json.load(open(path))
    expect(check(rec) == [], f"validator accepts {os.path.basename(path)}")
    expect("DISCLOSURE REQUIRED" in decide(rec), f"consumer generates disclosure for {os.path.basename(path)}")

sabor = json.load(open(f"{ROOT}/fixtures/sabor-conflicting.json"))
expect(check(sabor) == [], "validator accepts the conflicting fixture")
expect(decide(sabor).split(": ", 1)[1].startswith("CONFLICT FLAGGED"), "consumer flags the SABOR conflict")

old = json.load(open(f"{ROOT}/fixtures/crmls-superseded.json"))
expect(check(old) == [], "validator accepts the superseded fixture")
expect("SUPERSEDED" in decide(old), "consumer names the superseding record")

unk = json.load(open(f"{ROOT}/fixtures/example-unknown.json"))
expect(check(unk) == [], "validator accepts the unknown fixture")
expect("INSUFFICIENT INFORMATION" in decide(unk), "consumer refuses to guess on unknown")

inv = json.load(open(f"{ROOT}/fixtures/invalid-record.json"))
expect(len(check(inv)) >= 3, "validator rejects the invalid fixture with multiple errors")

print("\n%d failure(s)" % len(fails))
sys.exit(1 if fails else 0)
