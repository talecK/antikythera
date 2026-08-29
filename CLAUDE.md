# Antikythera — Discourse Gap Engine

Read `discourse-gap-engine-brief.md` fully before any work. It is the complete
project state: thesis, prior art, architecture, experiment protocol, open
questions.

## Decisions made (settled — do not relitigate unless explicitly reopened)

1. HN backtest first, before any product/niche commitment
2. Edge formation = primary eval; price/engagement secondary
3. No selling until signal strength known
4. Two-domain validation for generality
5. Crypto and health excluded
6. No formal bakeoff: smoke test + 2–3 parallel extractors, pre-registered primary
7. Control plane (Claude) / data plane (pinned batch model) split; never bulk-extract via agent sessions
8. Cache raw extractions immutably; iterate granularity downstream only

## Working rules

- "Open questions" in the brief are the live research frontier.
- Pre-registration discipline: primary extractor, eligible-pair spec, k values,
  and fold boundaries are written down (in `preregistration.md`) before any
  eval is run. Filter/pull SQL lives in `sql/` and is part of the spec.
- Leakage controls: embedding model predates eval window; no lookahead
  anywhere; every ingested row keeps its source timestamp.
- Data lands in `data/` (gitignored). Raw extractions are immutable, cached
  per (doc, extractor).
- Communication: terse, conclusions first, numbered lists, execution over
  explanation.
