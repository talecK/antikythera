# Paper 2 seed — "Watching the walls go up" (written 2026-08-31, session antikythera-cf)

Purpose: everything a fresh session needs to take the WSB transition
observation from paper 1 to a registered study, without this session's
context. Read with pipeline/RUNBOOK_parallel_pull.md (acquisition
mechanics, from session antikythera-27). Owner has approved the
direction; nothing below is registered yet.

## The observation (paper 1 Sec 6.3; gate table commit 1386fc0)

Suppressed ticker pairs co-mention below chance everywhere we measured,
EXCEPT wallstreetbets pre-GME:

| cell | seg z | obs/null |
|------|------:|---------|
| WSB fold A (build 2017-18, eval 2019) | **-0.2** | 150/152 — exactly chance |
| WSB fold B (build 2022-23, eval 2024) | **-8.7** | 369/596 — walled |
| DD fold A / fold B | -10.0 / -16.3 | deepened |
| HN (author/thread, run 8) | -9.2..-162 | walls everywhere |

Fold A's at-chance is well-measured: a DD-sized effect would have shown
z ~ -7 there. So the one wall-free community we ever observed grew
walls somewhere between 2019 and 2024. This is the only observed
TRANSITION in the whole research program — everything else is static.

## Why paper 1 could not claim it (all three must be neutralized)

1. Era confound: folds sit on opposite sides of the 2020-21 COVID+GME
   regime break by design.
2. Provenance confound: fold A is all-API (pulled 2026, post-deletion);
   fold B build is part archival-dump (captured near post time). The
   sources agree 99.94% on an overlap window (pipeline/
   provenance_check.py, gate amendment dae3a1c) but the seam aligns
   with the fold boundary.
3. Post-hoc: the DD-vs-MEME split was exploratory; no registered
   prediction existed. Frozen rule applied: reported as measured, no
   interpretation stretch.

## The design (two parts, one acquisition)

Acquisition: complete WSB via API, 2019-01..2024-12, one source, one
pull era. Serves both parts. Outcome-blind; may run before
registration. See the runbook.

Part A — provenance-hardening (confirmatory, cheap): rebuild fold B
with the dump months replaced by API months (uniform provenance both
folds), recompute the gate table WSB cells under the frozen gate
criterion (per-pair label-shuffle p99, R=100, seed 20260831 — reuse
eval/run_gate.py, which imports run_eval8.binom_sf_ge). Expected if
transition is real: fold B WSB z stays strongly negative. This removes
confound 2 only.

Part B — the transition study (the paper): rolling-window segregation
on continuous single-source WSB data. Sketch to be frozen in the
registration BEFORE any window is computed:
- Document = (author, quarter) as everywhere; rolling build/eval
  windows stepped quarterly (exact window lengths TBD in registration;
  shorter than the gate's 2y/1y to localize the transition, subject to
  an outcome-blind density check — eligible-pair counts per window must
  be published in the registration before any segregation z is seen).
- Statistic: the run-8 sub-chance total z per window (well-powered);
  formation counts secondary.
- REGISTERED PREDICTIONS to freeze (candidates; sharpen before
  committing): (P1) there exists a transition — early windows |z| < 3,
  late windows z <= -5; (P2) timing — the transition onset lies within
  [2021-01, 2021-12] (the GME event is 2021-01; moderation/structure
  changes followed through 2021); (P3) DD stratum shows no comparable
  discontinuity (its deepening is gradual). Any timing claim sharper
  than P2 must name its source BEFORE looking (e.g. dated WSB
  moderation-rule changes from subreddit wiki/mod announcements —
  collect these BEFORE computing windows, they are the causal-ordering
  anchors).
- Confound 1 (era) is not removable observationally; the design
  answer is WITHIN-community comparison across continuous time plus
  the DD-as-control contrast (P3). Say so plainly in the registration.

## Candidate mechanisms the timing can separate (from session discussion)

- Scale/fragmentation: WSB grew ~30x in Jan 2021; if walls = internal
  tribalization, onset tracks the subscriber explosion (fast, Q1 2021)
  and correlates with cohort join dates.
- Governance: post-GME WSB added moderation, daily-thread containment,
  flair; if walls = topicality policing, onset tracks datable rule
  changes (likely lagging the event by months).
- Era narratives: market-wide sector stories sort attention; predicts
  parallel (smaller) DD discontinuity — P3 is its test.
- Speculative framing worth keeping OUT of the registration but in the
  discussion: chance-level mixing as cascade susceptibility (the
  unsegregated state was the GME substrate; the event destroyed the
  conditions for its own repetition).

## House rules that bind this study (paid-for lessons)

1. Registration committed BEFORE any outcome computation; density/
   coverage checks are outcome-blind and go in the registration.
2. The z>=2 Poisson criterion is RETIRED (R1 placebo, reports/
   pilot1_runs.md); only the label-shuffle machinery is valid.
3. Long stages log to FILES, never pipes. Anchor every git command
   with -C. Data stays out of git (data/ is gitignored; NVMe symlinks).
4. The repo has a private GitHub remote (origin, talecK/antikythera) —
   push after committing; NEVER rebase/rewrite (history is release
   material for paper 1).
5. Paper 1 (reports/paper1_draft.md, v0.2) is FINAL on this
   observation: reported as measured, no stretch. Paper 2 must not
   reopen it; cite it.

## Key commits for the fresh session

- 1386fc0 gate FINAL table; dae3a1c + 774fcb9 provenance amendments;
  63b72d9/58eb65b run 8 (criterion + HN result); 31bc9ab/eb4c74a R1-R4
  placebo suite; ddbcc20 paper v0.2.
