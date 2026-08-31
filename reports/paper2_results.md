# Paper 2 results — registered eval, first run (2026-08-31)

Eval: eval/run_paper2.py under preregistration_paper2.md (REGISTERED
99ffd9e, eval code 35914d2). Corpus: single-era API pull (98.08M rows,
amendment V1). Full per-cell table (204 cells: 3 B x 2 strata x 2
lenses): reports/paper2_windows_z.tsv. Log:
data/paper2/eval.log (NVMe). All numbers below are the registered
scorer's own output, verbatim.

## Registered verdicts (primary cell: B=4, union)

- **ONSET: eval window 2021Q2..2021Q3, onset time 2021-04-01**, zero
  reversions in 13 subsequent windows (rule allowed one).
- **P1 PASS** — >=2 consecutive |z|<3 windows before onset (2020Q2
  +0.8, 2020Q3 +1.6); >=2 consecutive z<=-5 at/after (-9.1, -10.0).
- **P2 PASS** — onset inside [2021-01, 2021-12].
- **P3 PASS** — DD/union never leaves walled territory (-6.7..-14.9,
  2020-2024); no cliff pair anywhere in 2020-2022.
- **Step fit (secondary)**: break before eval 2021Q2; near-tie set is
  {2021Q2} alone — no ambiguity at the 10%-SSE bar.

WSB primary z: -3.4, +0.8, +1.6, **+29.5, +23.5**, -9.1, -10.0, -7.5,
-5.9, -7.1, -6.9, -7.7, -4.6, -6.6, -5.3, -7.8, -9.6, -4.9, -6.8
(eval 2020Q1..2024Q3 starts, quarterly).

## Sensitivity (registered, no bars)

B=6 WSB/union reproduces the shape: +25.9/+37.0 at the GME windows,
flip at eval 2021Q2..Q3, walls in every later window. B=8 and cashtag
cells in the TSV; cashtag windows under 20 eligible pairs are marked
UNINFORMATIVE per the frozen rule.

## Secondary observation (formation counts; registered as secondary,
## no bar)

The only above-floor formation ever observed in this program, on any
platform, in any fold: WSB eval 2020Q4..2021Q1 formed 26 of 125
eligible pairs and eval 2021Q1..2021Q2 formed 55 of 316 (floor ~1%).
Every other window in six years: 0-8, mostly 0-2. DD formed 0-1
everywhere. The GME event registers as a massive, transient
suppressed-pair formation burst, after which formation dies and the
below-chance walls set in. The cascade-susceptibility framing was kept
out of the registration (seed doc, house rule) and belongs to the
discussion; it is noted here only as the shape the data took.

## Bounds on interpretation (from the registration, restated)

- Onset at 2021Q2 is the anchor amendment's NON-SEPARABLE case: the
  subscriber explosion (A2) and the governance overhaul (A4-A8) were
  both active. The timing supports the WSB-specific transition claim
  (P1+P2+P3); it does not pick a mechanism.
- Era confound is not removable observationally; the design's answer is
  the within-community continuous series + DD contrast, both delivered.
- Between-window z magnitudes are different-powered tests (census V3
  caveat): plot eligible-pair counts under the z series in the paper.
- Part A (provenance-hardened fold-B endpoint rebuild) is still owed
  before the paper claims the endpoint; it shares this corpus.
