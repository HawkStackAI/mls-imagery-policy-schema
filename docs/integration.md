# Integration and the maintained policy feed

## What this repository gives you

The format, a validator, a reference consumer, and five sample records. Enough to build against, evaluate the approach, and handle the boards in `samples/` today.

## What it does not give you

Current records for the other boards. MLS imagery policies are moving targets: boards adopt new rules (NTREIS, effective November 2026), supersede their own guidance (CRMLS, July 2026), and answer clarification questions that change what a record should say (HAR, November 2026). A snapshot ages from the day it is taken.

## The commercial offering

RELTO maintains the full database behind this schema as a commercial service:

- Continuously maintained policy records across US boards, in this exact format.
- Automated updates and machine-readable change notifications when a board amends a rule.
- Confirmation work: the maintainer's research program asks boards to confirm their rules and records who confirmed what, and when.
- Disclosure generation and hosted evidence records built on the same records.

The schema is free to implement under Apache 2.0, permanently. What the service sells is currency: you can maintain hundreds of MLS policy records yourself, or RELTO can maintain them for you.

## Evaluating the fit

Start with the samples and fixtures. If your product serves boards beyond the five samples, or your compliance posture cannot tolerate stale records, the maintained feed is the relevant conversation. Contact: RELTO via relto.app/contact. Pricing is established through those conversations, not published here, because the right shape (feed, notifications, generation) depends on the integration.
