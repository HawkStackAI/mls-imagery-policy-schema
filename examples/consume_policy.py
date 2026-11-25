#!/usr/bin/env python3
"""Minimal working implementation: turn a policy record into a decision.

Implements the uncertainty behavior table from the README. The one rule
that matters: never generate definitive disclosure instructions from an
unresolved policy.

Usage: python3 examples/consume_policy.py samples/beaches-mls.json
"""
import json, sys

PLACEMENT_TEXT = {
    "on_image": "Place the disclosure on the image itself.",
    "adjacent_to_image": "Place the disclosure on or directly adjacent to the image, and include the unaltered original adjacent in the listing.",
    "public_remarks": "Place the disclosure in the public remarks.",
    "private_remarks": "Place the disclosure in the private (agent) remarks.",
    "photo_description": "Place the disclosure in the photo description.",
    "link_url_or_qr_to_original": "Include a link, URL, or QR code to the unaltered original image.",
}

def decide(rec):
    status = rec.get("status")
    name = rec.get("board", {}).get("name", "unknown board")
    if status == "confirmed":
        req = rec["requirements"]
        if req["disclosureRequired"] is not True:
            return f"{name}: no disclosure requirement is confirmed in this record."
        steps = [PLACEMENT_TEXT[p] for p in req["placement"] if p in PLACEMENT_TEXT]
        if req.get("placementDetail"):
            steps.append("Board specific constraint: " + req["placementDetail"])
        if req["onImageText"] == "prohibited":
            steps.append("Do NOT put disclosure text on the image itself; this board prohibits it.")
        return f"{name}: DISCLOSURE REQUIRED. " + " ".join(steps)
    if status == "conflicting":
        return (f"{name}: CONFLICT FLAGGED. This record carries unresolved conflicts "
                f"({'; '.join(rec.get('conflicts', []))}). Do not generate disclosure "
                f"instructions from it until the conflict is resolved.")
    if status == "unknown":
        return f"{name}: INSUFFICIENT INFORMATION. No verified policy is on record; do not guess."
    if status == "superseded":
        return f"{name}: SUPERSEDED. Use the newer record instead: {rec.get('supersededBy', 'unnamed')}."
    if status == "unresolved_interpretation":
        return f"{name}: MANUAL REVIEW REQUIRED. The rule exists but its interpretation is unresolved."
    return f"{name}: UNRECOGNIZED STATUS {status!r}. Treat as insufficient information."

if __name__ == "__main__":
    rec = json.load(open(sys.argv[1]))
    print(decide(rec))
