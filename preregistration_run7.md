# Run 7 registration — scout class: bridge persistence + scout-weighted ranking (2026-08-30)

Question (Burt structural-holes framing): is early bridging of never-co-
mentioned concept pairs a persistent per-person trait ("scouts"), and does
scout identity predict which suppressed pairs form — the ranking signal
that pair-level features failed to provide in runs 3/5/Tier A?

Committed BEFORE any run-7 outcome is computed. Data: run5_author parquet,
author-quarter documents, hub guard 100, F>=20 concept set — all unchanged
from runs 5/6. Fold-1 universe (build 2015–16, eval 2017) is primary;
fold 2 is descriptive corroboration only (2015-only track records are too
thin; disclosed).

## Definitions
- BRIDGE EVENT: the first author-quarter co-mention EVER (within data start
  2015Q1) of a frequent-concept pair. All authors tied in the first quarter
  are its first-bridgers.
- TRACK-RECORD ERA (build-only, no eval contact): events whose first
  co-mention falls in 2015Q3–2016Q2 (2015Q1–Q2 excluded as left-censoring
  burn-in; window end leaves >= 2 quarters for catch-on).
- CATCH-ON (per event): >= 2 distinct OTHER authors co-mention the pair in
  strictly later quarters through 2016Q4.
- AUTHOR PRECISION: caught-on events / events, over that author's
  track-record events. QUALIFIED author: >= 5 events (per half for stage A;
  >= 5 total for stages B/C).
- SLOW-BRIDGER of an eligible suppressed pair: an author with both concepts
  in their build-era history but never in the same quarter (same-quarter
  would make the pair ineligible).

## Stage A — persistence (trait vs state); PRIMARY readout
- Split track-record era: half 1 = events first-bridged 2015Q3–Q4, half 2 =
  2016Q1–Q2. Authors qualified in BOTH halves: Spearman rho between their
  half-1 and half-2 precisions.
- Null: 1,000 permutations shuffling catch-on flags across events within
  each half (preserves per-author event counts and global rate);
  seed 20260830.
- PASS: observed rho > 95th percentile of the null.

## Stage B — telescope test (rank at freeze time, before any 2017 signal)
- Universe: fold-1 eligible suppressed pairs (364; outcome = run-5
  author-space formation, 70 formed).
- SCOUT ranker: pair score = max precision over its qualified slow-bridgers
  (0 if none; count reported).
- Controls: ACTIVITY ranker (same slow-bridgers, weight = event count —
  kills the "scouts are just active users" confound); common_neighbors;
  random (seed 20260830).
- Readout: P@50/100/200. PASS: scout beats random AND activity AND
  common_neighbors at k=50. (Base rate 19.2%; Wilson CIs reported.)

## Stage C — alert test (conditional propagation, the product shape)
- Among fold-1 eligible pairs whose FIRST eval-window (2017) co-mention has
  a qualified first-bridger: split by first-bridger max precision into
  top vs bottom tercile; compare full-year formation rates.
- PASS: top tercile > bottom tercile, Fisher exact p < 0.05 (one-sided,
  registered direction). Excluded-pair counts reported.

## Interpretation (registered)
- A passes, B or C passes: scout class exists and carries ranking signal —
  the detector regains a telescope layer through people; variant gate must
  treat author identity as first-class.
- A passes, B and C fail: bridging is a trait but not predictive at these
  n; report CIs, no stretch.
- A fails: bridging is state, not trait; scout products are dead; variant
  gate proceeds as census-only.
- Small-n honesty: stage B has 364 pairs / 70 formed; stage C likely
  100–250 pairs. Exact counts and CIs reported; no claims beyond the
  registered comparisons.
