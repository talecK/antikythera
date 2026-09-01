# Paper 2 results — registration-conforming run (2026-08-31, V4-corrected)

OPERATIVE VERSION. The first run (same day) omitted the registered
EXCLUDED_TICKERS filter; amendment V4 discloses the deviation and the
rule-bound correction path. First-run outputs are retained in
reports/paper2_windows_z_v1_superseded.tsv and _window_census_v1_
superseded.tsv and in this file's git history; every verdict below is
from the conforming rerun and every decision was re-derived by the
unchanged frozen rules (B-ladder re-decision committed pre-outcome at
80b3b37). Both runs agree on every verdict.

Eval: eval/run_paper2.py under preregistration_paper2.md (REGISTERED
99ffd9e; amendments V1-V4). Corpus: single-era API pull, 98.08M rows.
Full 204-cell table: reports/paper2_windows_z.tsv.

## Registered verdicts (primary cell: B=4, union) — scorer output verbatim

- **ONSET: eval window 2021Q2..2021Q3, onset time 2021-04-01**; zero
  reversions in 13 subsequent windows (rule allowed one).
- **P1 PASS** (2 consecutive |z|<3 before onset: 2020Q2 +1.5, 2020Q3
  +1.5; 2 consecutive z<=-5 at/after: -10.7, -9.0).
- **P2 PASS** (onset inside 2021).
- **P3 PASS** (DD/union -6.7..-15.7 throughout; no cliff pair).
- **Step fit (secondary):** break before eval 2021Q2; near-tie set
  {2021Q2} alone.

WSB primary z (eval starts 2020Q1..2024Q3, quarterly): -3.7, +1.5,
+1.5, **+28.6, +30.9**, -10.7, -9.0, -8.6, -5.9, -7.3, -4.9, -9.7,
-4.6, -7.7, -6.7, -7.2, -11.0, -5.3, -6.3.

## The excursion (both statistics, conforming run)

| cell (B=4/union) | n_elig | obs | z | formed | binom p |
|---|---:|---:|---:|---:|---|
| WSB eval 2020Q4-2021Q1 | 124 | 1125 | **+28.6** | 24 | 1e-23 |
| WSB eval 2021Q1-2021Q2 | 318 | 2891 | **+30.9** | 61 | 1e-57 |
| DD eval 2020Q4-2021Q1 | 145 | 570 | -7.7 | 1 | 0.77 |
| DD eval 2021Q1-2021Q2 | 211 | 522 | -8.6 | 0 | 1.0 |

The fusion is WSB-only: DD stays walled straight through the squeeze.
Formation counts are registered secondary (no bar, underpowered by
design) — the excursion claim rests on the primary z.

## Excursion placebo (post-registration robustness; commit 7bef4a2)

40 truth-null replicates (outer label-shuffle, full registered
statistic per replicate, per-rep seeds documented) in the exact
excursion regime:

| window | placebo z mean | sd | min | max | formed max | real |
|---|---:|---:|---:|---:|---:|---|
| k=3 | +0.47 | 1.18 | -1.45 | +3.25 | 4 | +28.6 / 24 |
| k=4 | +0.30 | 0.99 | -1.71 | +2.53 | 7 | +30.9 / 61 |

The machinery does not manufacture the excursion under null: the real
values sit ~24-31 placebo SDs out. Answers the densification concern
(paper-1 R1 history) for this specific regime.

## Part A — provenance-hardened fold-B endpoint (expectation MET)

Frozen gate criterion on the uniform-API corpus, fold B, exclusion
applied, vs gate v2 references (post-review, f89cb2b):

| cell | n_elig | z (uniform API) | z (gate v2, mixed) | formed | binom_p |
|------|-------:|---------------:|-------------------:|-------:|--------:|
| MEME/union | 210 | **-9.40** | -9.0 | 0 | 1.00 |
| ALL/union  | 479 | **-21.57** | -17.7 | 2 | 0.95 |
| DD/union   | 281 | **-16.41** | -17.1 | 0 | 1.00 |

Registered expectation (MEME z <= -3) met with margin; eligible counts
now track the gate v2 census (210 vs 209). Confound 2 (provenance) is
removed from the paper-1 Sec 6.3 endpoint. Cashtag consistent
(-8.5/-10.1/-3.1).

## Census consistency cell (V4 addendum target)

Corrected census build-2019 WSB/union docs = 44,013 vs gate v2 fold-A
MEME eval docs 44,012 — agreement to one document in 44K between
independently pulled corpora; near-exact, not identical, reported as
such.

## Sensitivity (registered, no bars)

B=6 and B=8 curves in the TSV reproduce the shape (excursion then flip
at the same eval window); cashtag windows under 20 eligible pairs are
UNINFORMATIVE per the frozen rule.

## Discussion-section notes (NOT registered claims)

- Three-regime arc: one community, five years, all three states —
  walled (below chance), chance-level, cascade-fused (above chance).
  The cascade-susceptibility reading (chance-mixing as substrate; the
  event fuses everything; walls are the scar) is describable, not
  speculative; mechanism attribution is NOT claimed (below).
- Pre-cascade generality: chance-level holds through 2020Q3, so paper
  1's fold-A 2019 chance result was not a special year (inference
  belongs to this paper; paper 1 cites, d0aa9d6/d1cbfc1 there).

## Bounds on interpretation (registered, restated)

- Onset 2021Q2 is the anchors amendment's NON-SEPARABLE case (scale A2
  and governance A4-A8 both active): the timing supports the
  WSB-specific transition claim, not a mechanism.
- Era confound answered by design (continuous within-community series +
  DD contrast), not eliminated.
- Between-window z magnitudes are different-powered tests (eligible
  pairs 45..498): plot pair counts under the z series.
